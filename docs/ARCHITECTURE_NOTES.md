# LearnHouse Architecture Notes

How upstream LearnHouse is put together, written so the Personal Learning OS features (starting with the Inbox) can be added without fighting it.

| | |
|---|---|
| Source | `learnhouse/learnhouse`, branch `dev`, commit `5e28b07` |
| Method | Read from source on 2026-10-02 (cloud session, not yet run) |
| Status | **Draft.** Items marked ⏳ get confirmed during the Phase 0 run on DavidLab |

---

## 1. The big picture

```text
Browser
  │
  ▼
apps/web  (Next.js, :3000)
  │  /api/v1/*  → proxied by app/api/v1/[...path]/route.ts
  ▼
apps/api  (FastAPI, :1338)  ──────────────►  PostgreSQL 16 + pgvector (:5432)
  │   prefix /api/v1                            Redis 8 (:6379)
  │                                             AI providers (Pydantic AI)
  ▲
apps/collab (Hocuspocus + Yjs, :4000)
  verifies the same JWT, saves editor docs through the API
```

- **Web never talks to Postgres.** Every request goes browser → Next.js → FastAPI. The Next.js route `app/api/v1/[...path]/route.ts` is a thin proxy that forwards headers and body as-is (a "backend-for-frontend" pattern).
- **Collab** is the real-time editor server. It checks the user's JWT with the same `LEARNHOUSE_AUTH_JWT_SECRET_KEY` as the API (HS256), which is why the CLI writes that secret into both env files.
- **Deployment mode** (`src/core/deployment_mode.py`) is one of `saas`, `ee` or `oss`. A dev run without `--ee` sets `LEARNHOUSE_DISABLE_EE=1`, so we run **OSS mode**: SSO, audit logs, payments, advanced analytics and SCORM are blocked by the backend itself.

## 2. Repo map

| Path | What lives there |
|---|---|
| `apps/api/app.py` | FastAPI app. Mounts `src/router.py` (`/api/v1`). |
| `apps/api/config/config.py` + `config.yaml` | All settings. **Env vars override YAML.** `load_dotenv()` reads `apps/api/.env`. |
| `apps/api/src/db/` | SQLModel tables (one file per model, `courses/` subfolder for the course tree). |
| `apps/api/src/routers/` | FastAPI routers (thin: auth + validation, then call a service). |
| `apps/api/src/services/` | Business logic, grouped by domain (`courses/`, `trail/`, `ai/`, `search/`, …). |
| `apps/api/src/security/` | Auth (`auth.py`), RBAC (`rbac/`), CSRF, org access, feature checks. |
| `apps/api/migrations/` | Alembic (68 revisions at this commit). |
| `apps/api/src/tests/` | Pytest suite (in-memory SQLite, see §8). |
| `apps/web/app/` | Next.js App Router routes. Learner pages under `orgs/[orgslug]/(withmenu)/`, admin under `orgs/[orgslug]/dash/`. |
| `apps/web/components/` | UI. Menus in `components/Objects/Menus/`, org settings in `components/Dashboard/Pages/Org/`. |
| `apps/web/services/` | Typed API client functions used by pages and components. |
| `apps/collab/src/index.ts` | Hocuspocus server. |
| `apps/cli/src/commands/dev.ts` | What `npx learnhouse dev` actually does (§3). |
| `apps/e2e/` | Playwright suite (`core/` fixtures + `features/`). |

## 3. How `npx learnhouse dev` runs things

| Step | Detail |
|---|---|
| 1. Env check | Looks for required vars in `apps/api/.env`, `apps/web/.env.local`, `apps/collab/.env`. If any are missing it **asks interactively** "Apply dev defaults?" and appends only the missing ones (existing lines are kept). |
| 2. Admin prompt | On first run (no containers yet) it **asks interactively** for admin email and password unless `--admin-email` / `--admin-password` are passed. |
| 3. Containers | Writes `.learnhouse/docker-compose.dev.yml`, project `learnhouse-dev`: `learnhouse-db-dev` (`pgvector/pgvector:pg16`, user/pass/db all `learnhouse`) and `learnhouse-redis-dev` (`redis:8.6.1-alpine`). They keep running after you quit. |
| 4. Dependencies | `bun install` in web and collab, `uv sync` in api (downloads Python 3.14.7). |
| 5. Services | api `uv run python app.py` (:1338), web `next dev --turbopack` (:3000), collab `tsx watch src/index.ts` (:4000). Sets `LEARNHOUSE_DEVELOPMENT_MODE=true` itself. |

Generated secrets: `LEARNHOUSE_AUTH_JWT_SECRET_KEY` is random. `COLLAB_INTERNAL_KEY` defaults to a fixed dev string (`dev-collab-internal-key-change-in-prod`), which is fine locally and must change before any exposure.

Stop containers: `docker compose -f .learnhouse/docker-compose.dev.yml -p learnhouse-dev down`.

## 4. Data model (the parts we care about)

```text
Organization ─┬─ Course ── CourseChapter ── Chapter ── ChapterActivity ── Activity
              │                                                         (type + subtype)
              ├─ Folder ("Library", nestable) ── FolderContent (any resource, by prefixed UUID)
              ├─ OrganizationConfig  (JSON: features, admin toggles, menu, signup)
              └─ User (via UserOrganization + Role)

User ── Trail ── TrailRun (per course) ── TrailStep (per completed activity)
Course ── CourseEmbedding (pgvector, 768 dims, per chunk)
```

- **Activity types:** `TYPE_DYNAMIC` (Tiptap page / markdown / embed / resource), `TYPE_VIDEO` (**`SUBTYPE_VIDEO_YOUTUBE`** or hosted), `TYPE_DOCUMENT` (PDF/doc), `TYPE_ASSIGNMENT`, `TYPE_CUSTOM`, `TYPE_SCORM`.
- **Progress = Trail.** A `TrailRun` (`RUN_TYPE_COURSE`, status in-progress/completed/paused/cancelled) holds `TrailStep`s for finished activities. It is completion tracking, not mastery: there is no concept of topic, confidence or evidence yet.
- **Collections no longer exist.** Upstream dropped them (migrations `d4e5f6a7b8c9_drop_collections_tables`, `7f2b9d1c3e4a_…drop_collections`) and replaced them with **Folders**, shown as the **Library**. Folders nest (`parent_folder_id`) and hold any resource through `FolderContent.resource_uuid`, whose prefix names the type (`course_`, `podcast_`, `media_`, …). Learning paths like "AI Engineer Path" would be Library folders today.
- **Prefixed UUID convention.** Resources are referenced polymorphically by prefixed UUIDs (also used by `UserGroupResource` and `ResourceAuthor`). A new resource type such as `inbox_` could follow it and sit in Library folders.
- **Org feature config** (`src/db/organization_config.py`) is a JSON blob, so toggling features needs no migration. See §7.

## 5. Auth

- JWT access token (8 h) in cookie `LH_access`, or an `Authorization: Bearer` header (header wins). Refresh tokens last 14–30 days.
- Algorithm is pinned to HS256 on decode (prevents algorithm-confusion attacks).
- CSRF protection on cookie-authenticated requests (`src/security/csrf.py`).
- RBAC through roles per org (`src/security/rbac/`).
- Sign-in methods per org: password, magic link, Google, SSO (SSO is EE-only). Restrictable with `admin_toggles.security.allowed_auth_methods`.

## 6. AI and RAG

| Piece | Where | Notes |
|---|---|---|
| Provider layer | `src/services/ai/llm/provider.py`, `client.py`, `tiers.py` | Pydantic AI. Providers: google, openai, anthropic, deepseek, moonshot, mistral, openrouter, bedrock, ollama. Three tiers: fast / standard / pro. |
| Embeddings | `src/services/ai/llm/embeddings.py` | Follow `LEARNHOUSE_AI_EMBEDDING_PROVIDER`, else the chat provider. Anthropic has none, so it **falls back to Google** when `LEARNHOUSE_GEMINI_API_KEY` is set. OpenAI embeddings reuse `LEARNHOUSE_AI_API_KEY`. Ollama default model `nomic-embed-text`. |
| Vector store | `src/db/course_embeddings.py` | `Vector(768)`. Changing dims needs a migration and a re-index. |
| Indexing | `src/services/ai/rag/embedding_service.py` → `embed_course_content()` | Triggered when activities are saved, or manually via `POST /api/v1/ai/rag/index`. |
| Retrieval | `src/services/ai/rag/query_service.py` | Scoped by `org_id`, optionally `course_id`. |
| Chat | `src/routers/ai/ai.py` (activity chat, editor chat), `rag.py` (`/rag/chat`, sessions) | The learner-facing chat is **Copilot** (`/copilot` page + bubble). |

**Important for later phases:** `CourseEmbedding.course_id` is a required foreign key. RAG over notes, Inbox items or topics will not fit this table as-is. That's a Phase 4 design decision.

## 7. What can be hidden without code

Org-level toggles live in `OrganizationConfig` and are edited from **Dashboard → Organization settings** ⏳ (confirm screen names).

| Want hidden | How | Code needed? |
|---|---|---|
| Payments, Store | OSS mode blocks payments; Store menu item only shows when payments is enabled | No |
| SSO, audit logs, SCORM, advanced analytics | OSS mode | No |
| Communities, Podcasts, Boards, Playgrounds | `features.*.enabled` / `admin_toggles.*.disabled` (Podcasts, Boards, Playgrounds are off by default) | No |
| Public signup | `admin_toggles.members.signup_mode = "inviteOnly"` | No (the API rejects signups with HTTP 403, not just the UI) |
| Sign-in methods | `admin_toggles.security.allowed_auth_methods = ["password"]` | No |
| Top menu items | `menu.items` (courses, library, podcasts, communities, playgrounds, store, custom) | No. Custom links could even point at `/inbox` later |
| Multi-org / tenancy | Tenancy defaults to `single` on localhost | No |
| Certificates page, Hub/billing routes, Explore/marketing pages | Not covered by a toggle found so far | ⏳ Check while exploring. Phase 1 code task if visible |

Notes:
- The web app **ignores** `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG`. Tenancy comes from the backend via the `LH_tenancy` cookie.
- `LEARNHOUSE_USE_DEFAULT_ORG` is superseded by `LEARNHOUSE_TENANCY` (`single` | `multi`).

## 8. Migrations, tests and lint

| Task | Command (from the app folder) | Notes |
|---|---|---|
| Schema on a fresh DB | none, automatic | Startup runs `SQLModel.metadata.create_all` plus `CREATE EXTENSION vector`. **Alembic is not run.** |
| Alembic status | `uv run alembic current` | Shows **no revision** on a fresh dev DB (never stamped). Expected. |
| Before the first custom migration | `uv run alembic stamp head` | Marks the create_all schema as current so autogenerate only diffs our changes. |
| New migration | `uv run alembic revision --autogenerate -m "add inbox_item"` | Review the generated file by hand. |
| Apply | `uv run alembic upgrade head` | |
| API tests | `uv run pytest src/tests/ -q` | `conftest.py` sets `TESTING=true` and uses **in-memory SQLite**, so tests don't need Postgres. CI adds coverage (`--cov-fail-under=25`) and needs `ffmpeg`. |
| API lint | `uvx ruff check .` | Ruff is configured in `pyproject.toml` but not a dependency, hence `uvx`. CI pins the version. |
| Web tests | `bun test tests` | |
| Web lint | `bunx eslint .` | Report-only upstream (existing backlog). |
| Web typecheck | `bunx next typegen && bunx tsc --noEmit` | |
| E2E | `apps/e2e` (Playwright) | ⏳ Confirm how to point it at the dev stack. |
| Lockfiles | `scripts/lockfiles.sh` | After touching `package.json` or `pyproject.toml`. CI checks them. |

⚠️ Because startup uses `create_all`, a new SQLModel table **appears in dev even without a migration**. Missing migrations stay invisible locally. For the Inbox, always generate and run the migration, and test `alembic upgrade head` on a fresh DB.

## 9. Search

`src/services/search/search.py` does case-insensitive `ILIKE` matching on names, descriptions and tags (courses, folders, communities, discussions, playgrounds, podcasts). It does **not** search activity content, and it is not full-text or semantic. Making search a flagship feature (CLAUDE.md) means building on this, likely with Postgres full-text and pgvector.

## 10. Where the Personal Learning OS plugs in

| Our feature | Closest upstream piece | Starting thought |
|---|---|---|
| Learning Inbox | none | New `InboxItem` model + router + `/inbox` page, kept in its own module |
| YouTube Learning | `Activity` with `SUBTYPE_VIDEO_YOUTUBE` | Decide: resource outside courses, or wrap upstream activities |
| Progress / mastery | `Trail` (completion only) | Topic-level progress needs new tables, can read Trail as evidence |
| Knowledge search | `services/search` (ILIKE) | Extend, don't replace |
| AI tutor over notes | RAG is course-scoped | New embedding source or generalised table (Phase 4 decision) |
| Nav entries | `menu.items` custom links | Possibly add Inbox to the menu with zero upstream UI edits |
| Learning paths / Roadmaps | Library `Folder` (Collections are gone) | Use folders first; a Roadmap model only if folders can't express order and prerequisites |
