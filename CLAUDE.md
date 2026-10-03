# Project

**Personal Learning OS**: a personal technical learning platform built on a fork of [LearnHouse](https://github.com/learnhouse/learnhouse).

It is not just an LMS. It combines:
LMS + Personal Knowledge Base + Progress Tracker + Project Journal + AI Tutor + Knowledge Graph + Technical Reference Library.

- One user (me), personal-first. Multi-user comes only after the personal version is excellent.
- LearnHouse Core is **AGPL-3.0**. Review the AGPL and Enterprise licensing before any commercial or hosted distribution.
- The project doubles as my curriculum for Python, TypeScript, React/Next.js, FastAPI, PostgreSQL, Docker, Redis and RAG.

# Mission

> I consume and build a lot, but valuable knowledge gets scattered across chats, videos, courses, repos, notes and projects.

Turn everything I learn into **organized, connected, searchable, reviewable, long-term knowledge**.

Core loop. Every feature must strengthen it:

```text
CAPTURE → LEARN → UNDERSTAND → BUILD → DOCUMENT → CONNECT → REVIEW → REMEMBER
```

**Success** = I can answer without digging through chats, bookmarks or repos: *What did I learn six months ago? Where? What projects used it? What do I understand well? What have I forgotten? What should I review? What next? How does it connect to everything else I know?*

# Product Principles

- Every feature must improve at least one of: **Capture, Understanding, Connection, Practice, Progress, Application, Retention, Retrieval**. If it doesn't, don't build it.
- Capture must be extremely low friction. Save now, organize later.
- AI-generated content (summaries, concepts, questions) is **always editable**. My own explanation outranks the AI summary.
- Progress is based on **evidence**, never vanity percentages. Projects and labs count most.
- Projects, notes, topics and resources are first-class learning objects, not only courses.
- Don't build things just because AI can build them or because they look impressive.

# LearnHouse Foundation

Approach: **Install → Run → Explore → Understand → Document → Extend.** Never rewrite LearnHouse functionality without a clear technical reason.

Monorepo (upstream):

```text
apps/web     Next.js + React + TypeScript + Tailwind + Tiptap editor
apps/api     Python FastAPI + SQLModel + Alembic (config: apps/api/config/config.py)
apps/collab  Hocuspocus + Yjs + WebSockets (realtime editing)
apps/cli     `npx learnhouse` CLI (dev env, setup, env templates)
apps/e2e     end-to-end tests
docker/      Docker / Compose assets
```

Keep LearnHouse's concepts: **Course → Chapter → Activity**, and the **Library** (nestable **Folders**) for learning paths (e.g. "AI Engineer Path", "Cybersecurity Path"). Upstream removed Collections; Folders replaced them.

**Run it whole, hide what I don't need.** Don't delete upstream code, because that breaks merges. Turn features off through config, and remove them from navigation and the UI:

| Hide / disable | How |
|---|---|
| Payments (Stripe) | Leave all `LEARNHOUSE_STRIPE_*` unset. OSS mode (no `--ee`) blocks payments; the Store menu item only shows when payments is on |
| Multi-org / SaaS / tenancy | `LEARNHOUSE_SAAS=false`, `LEARNHOUSE_TENANCY=single` (the default on localhost), one org only |
| Public signup, user/role management, invites | Single user (me). Org settings: signup `inviteOnly`, sign-in methods `password` only. Hide member-admin screens. |
| Communities, podcasts, boards, playgrounds | Org feature toggles (the last three are off by default) |
| Email (Resend/SMTP) | Leave unset. Use a local admin account. |
| Analytics (Tinybird), Sentry | Leave unset. |
| Marketplace / public course catalog, certificates, payments-related pages | Hide from navigation. |
| Real-time collaboration (collab server) | Keep it running if the editor needs it, but no multi-user features in the UI. |

**Keep**: courses, chapters and activities, the Tiptap editor, the Library (folders), search, the AI/RAG layer (Copilot) and progress tracking (Trail).

Hiding order: env flags → OSS mode → org settings (database, no code) → upstream UI edits only in Phase 1 for what's left. See `docs/DECISIONS.md` D-004 and `docs/ARCHITECTURE_NOTES.md` §7.

# Architecture

```text
User → Next.js (apps/web) → FastAPI (apps/api) → PostgreSQL + pgvector
                                   ↘ Redis          ↘ AI layer (Pydantic AI, LlamaIndex)
```

- **One backend**: FastAPI. No second backend, no microservices.
- **One database**: LearnHouse's PostgreSQL + pgvector. Do not add Neo4j, Pinecone, MongoDB or Supabase as production dependencies. Study them separately if curious.
- **Knowledge graph = Postgres relationship tables**, e.g. `Topic → related/prerequisite → Topic`, `Resource → teaches → Topic`, `Project → uses → Topic`. Revisit only if Postgres becomes a proven limitation.
- **New models only when their feature enters the roadmap.** Likely candidates: `InboxItem`, `Resource`, `Topic`, `TopicRelationship`, `Project`, `LearningLog`, `UserTopicProgress`, `Review`, `VideoTranscript`, `CommandReference`, `LearningGoal`.
- Endpoints are small, typed (Pydantic/SQLModel), documented and tested. Schema changes go through **Alembic migrations**.

# Core Product Areas

- **Learning Inbox** (first custom feature): one-click capture of a YouTube URL, article, GitHub repo, course, PDF, docs, idea, lab, project, note or command. Later: Inbox → review → summarize → tag → connect → Knowledge Base.
- **YouTube Learning**: URL → metadata → transcript → AI summary → concepts → notes → review questions → topic links. Store title, channel, URL, thumbnail, transcript, summary, key concepts, my notes, timestamps, questions, related topics and status.
- **Knowledge Topics**: reusable concepts independent of courses (Docker, RAG, OAuth, …). Each has a definition, why it matters, core concepts, examples, commands, related topics, resources, projects, lessons, my notes, confidence and next step.
- **Knowledge Graph**: topics connected by typed relationships (e.g. JavaScript → React → Next.js; Identity → Entra ID → OAuth/OIDC → Conditional Access).
- **Projects**: what I built, why, tech used, problems, fixes, lessons, screenshots, repo, related concepts, next improvements. They are linked to topics and are strong progress evidence.
- **Resource Library + Commands**: resources attach to topics (no giant bookmark pile). Command cheat sheets are searchable.
- **Dashboard**: Current Focus · Continue Learning · Review Today · Active Projects · Recent Learning · Learning Domains.
- **Search**: one box across topics, courses, videos, notes, projects, resources, commands and transcripts. It should become a flagship feature.
- **Navigation**: Dashboard · Learn · Knowledge · Projects · Roadmaps · Inbox · Resources · Progress. Later: Quiz · Knowledge Graph · AI Tutor. Don't add more prematurely.
- Later: Roadmaps (visual paths), Learning Journal (daily/weekly log), Weekly Review.

# Learning Model

- **Status per topic**: Not Started → Learning → Practicing → Comfortable → Confident.
- **Evidence**: read/watched < quiz < lab < personal explanation < review < project usage / repeated usage.
- **Mastery** is per sub-skill (e.g. Docker: Volumes = Strong, Networking = Developing), not "Docker 82%".
- **Retention** (later): active recall, AI-generated and manual questions, spaced repetition, weak-topic detection.
- **Domains**:
  - AI: LLMs, workflows, agents, RAG, embeddings, vector DBs, MCP, tool calling, skills, memory, evals
  - Python (primary): fundamentals, automation, APIs, Flask, FastAPI, Django, testing, security scripting
  - JS/TS (secondary, growing): fundamentals, async, DOM, npm, TypeScript, React, Next.js
  - Backend: APIs, FastAPI/Flask/Django, PostgreSQL, Supabase, auth, Redis
  - Frontend: HTML, CSS, JS, TS, React, Next.js, Tailwind, UI/UX, accessibility
  - DevOps: Linux, Bash, Git/GitHub, Docker/Compose, CI/CD, GitHub Actions, deployment, monitoring, Grafana
  - Cybersecurity: networking, IAM, Entra ID, OAuth/OIDC/SAML, Conditional Access, Sentinel, Defender, KQL, threat hunting, vuln management, Zero Trust
  - Home Lab: Docker, Linux, networking, storage, Jellyfin, Grafana, n8n, remote access

# Development Rules

1. Understand existing code before modifying it. Read and trace first.
2. Extend LearnHouse; don't recreate what it already does.
3. No unnecessary dependencies, microservices or databases.
4. PostgreSQL + existing pgvector first. FastAPI stays the backend.
5. Simple, maintainable code over clever code.
6. Preserve upstream compatibility. Keep custom code isolated (own modules/routers/components where practical) so upstream merges stay easy.
7. Build **one useful feature at a time**, end-to-end, then test the important user flows (API tests + a Playwright check).
8. Git: fork `Darideivi/learnhouse`, with `upstream` = learnhouse/learnhouse. Use feature branches. Commit or push only when asked.
9. Record important architecture decisions in `docs/DECISIONS.md` (decision, why, alternatives, trade-offs, date, revisit-when).
10. Never commit secrets. `.env` is gitignored, and `.env.example` holds placeholders only.

## Learning While Building

After every meaningful change, explain briefly:
**What changed? Which files and why? What framework/programming concept is involved? What should I study next?**
I want to understand the code, not just receive it. Suggest a concept to study when relevant. Infrastructure problems (Docker, env, networking) are learning material too, so note them in `docs/LEARNING_LOG.md`.

# UI / UX Direction

A professional developer tool, in the spirit of **Linear, Vercel, GitHub, Notion and modern technical docs**. Stay consistent with LearnHouse's design language.

- Clean, minimal, fast, dark-mode friendly, strong typography, generous spacing, clear hierarchy, responsive and accessible.
- Avoid: childish gamification, heavy gradients, card overload, generic AI dashboards, clutter, and decorative UI that adds nothing.
- Mobile (no parity needed): watch, read, take notes, review, quiz, search. Desktop: create, organize, manage projects, graph, admin.

# AI / RAG Direction

- **Reuse LearnHouse's AI layer first** (provider-agnostic LLM layer, Pydantic AI, LlamaIndex, pgvector RAG). Investigate how it works before extending it.
- Providers are configured through `LEARNHOUSE_AI_*` env vars. Current choice: **Anthropic for chat, Google Gemini for embeddings** (`gemini-embedding-001`, **768 dims** to match the `Vector(768)` column; Anthropic has no embeddings API and upstream falls back to Gemini). Ollama embeddings are a proposed alternative (D-006). Never hard-code a provider into a custom feature.
- Upstream RAG is **course-scoped** (`CourseEmbedding.course_id` is required). RAG over notes, Inbox items or topics needs a design decision in Phase 4.
- The tutor (later) does RAG over my notes, videos/transcripts, courses, projects and docs. It uses learner context (current focus, known/weak topics, projects, goals) to explain new things through what I already know (e.g. Kubernetes through Docker).
- Pipeline: content → chunking → embeddings → pgvector → retrieval → tutor. No separate vector DB.
- Ideas borrowed from INDEX 0 (index-0.in; closed source, so ideas only, no code):
  - **Coach, not answer machine**: the tutor gives hints that escalate when I'm stuck and reveals full answers last.
  - **Local AI option**: support Ollama (small local model on the homelab) so everyday AI costs nothing. Cloud models are for heavy tasks.
  - **Learning stages**: a topic moves through frame → intuition → practice → analyze → improve → review, which maps onto the status ladder.
- Use deterministic code for fixed steps and LLM calls only where judgment is needed. Prefer workflows over autonomous agents unless the path is truly dynamic.

# Tooling (Claude Code)

- **ECC is the primary workflow** ([affaan-m/ECC](https://github.com/affaan-m/ECC), enabled in `.claude/settings.json`). Don't layer other orchestration frameworks (Superpowers, Agent Skills, GStack, Spec Kit, Task Master) on top of it for the same task.
  - Plan: `/ecc:plan`, `ecc:planner` / `ecc:architect`, `ecc:architecture-decision-records` → `docs/DECISIONS.md`
  - Understand LearnHouse: `ecc:codebase-onboarding`, `ecc:code-explorer`, `ecc:documentation-lookup`
  - Build: `/ecc:feature-dev`, `ecc:tdd-guide`, `ecc:fastapi-patterns`, `ecc:database-migrations`, `ecc:postgres-patterns`, `ecc:react-patterns`
  - Review: `ecc:python-reviewer` / `ecc:fastapi-reviewer` (API), `ecc:typescript-reviewer` / `ecc:react-reviewer` (web), `ecc:database-reviewer` (migrations), `ecc:security-reviewer` (auth, ingestion, secrets)
  - Verify: `ecc:e2e-runner` (Playwright), `/ecc:quality-gate`, `ecc:verification-loop`
  - ECC's GateGuard hook asks for facts before first writes/commands. Answer it, or add path globs to `GATEGUARD_EXEMPT_GLOBS` if it slows routine work.
- Complementary single-purpose tools (not orchestrators): **Serena** (semantic code nav), **Ponytail** (anti-overengineering), **Playwright CLI**, **UI/UX Pro Max**, **Impeccable** (polish after a feature works), **Frontend Design**, **Skill Creator** (later: `/add-learning`, `/analyze-youtube`, `/weekly-review`, …).
- Security tooling (Trail of Bits skills, Strix) comes later, and only against systems I own.

## Working unattended (`/goal`, handoffs, parked decisions)

- **Start of every session:** read `docs/STATUS.md`, then `docs/OPEN_QUESTIONS.md`. **End of every session or goal:** update `docs/STATUS.md` (done, next, blockers). The repo is the memory, so a fresh session never depends on an old chat.
- **Need a decision from David?** Add it to `docs/OPEN_QUESTIONS.md` with what it blocks and a sensible default, then continue with work that doesn't depend on it. Don't stop the whole run for one question. Use the default only when the blocked work is cheap to redo; otherwise leave that work for later.
- **Never do unattended:** anything needing David's password or real API keys, pushing or merging, deleting data, touching the existing homelab containers (n8n, Jellyfin, cloudflared, nginx). Park these in `OPEN_QUESTIONS.md`.
- **Long runs:** Claude Code auto-compacts when context fills. Before a big phase change, or after compaction, update `docs/STATUS.md` so nothing lives only in the conversation.
- **`/goal`** needs auto mode to run without approval prompts. Goals end on their own when credit runs out, so keep goals scoped to one phase and on the model the routing table says.

## Model routing (spend Fable credit only where it pays off)

Most tokens are spent in the **main session**, because every turn re-reads the whole conversation. So the main session runs the cheapest model that can do the job, and the big model is used for short, high-judgment steps.

| Tier | Model | Use for |
|---|---|---|
| **Heavy** | Fable (while credit lasts) | Architecture and design decisions, `/ecc:plan` for a new feature, data-model and migration design, final review of a finished feature, debugging that is still stuck after 2 attempts |
| **Standard** | Sonnet | Building from an approved plan, writing tests, running and fixing the stack, generating migrations, editing docs |
| **Light** | Haiku | Searching code (Explore), reading logs, summarising files, journal and learning-log entries |
| **Security** | Opus | `ecc:security-reviewer` and anything about auth, secrets or ingestion |

Rules for Claude:
1. When spawning a subagent, always pass `model` explicitly using this table. Never let a search or log-reading agent inherit Fable.
2. If the main session is on Fable and the next step is mechanical (installs, edits, test runs), say so in one line and suggest `/model sonnet`. If it's on Sonnet and a Heavy step comes up, spawn a Fable subagent for that step only.
3. If a Fable call fails for credit or billing reasons, use Opus for that role, tell David once, and keep going.
4. Keep Fable prompts tight: give file paths and `docs/ARCHITECTURE_NOTES.md` sections instead of having it re-read the codebase.

Session map:

| Session | Main model | Fable used for |
|---|---|---|
| Phase 0 run on DavidLab | Sonnet | Nothing (it's installs, logs and docs) |
| Answering the open design questions | Fable | The whole session (short and decisive) |
| Inbox design (`/ecc:plan`) | Fable | The whole session |
| Inbox build (TDD) | Sonnet | One final review subagent |
| Notes importer | Sonnet | Nothing |

Token savers:
- **Ponytail** (enabled in `.claude/settings.json`) keeps generated code minimal. Smaller diffs mean fewer tokens and less to review.
- **Graphify**: query `graphify-out/` before grepping. Building the graph is itself expensive (the GD Focus graph used ~292k tokens for 114 files; LearnHouse has ~1,900 source files). Build it **once, on Sonnet**, scoped to the folders we touch (`apps/api/src`, `apps/web/app`, `apps/web/components`, `apps/web/services`), and rebuild only after big upstream merges.
- `docs/ARCHITECTURE_NOTES.md` is the cheapest map of all. Read it before exploring.
- Use **graphify** for code maps: run `graphify .` on the LearnHouse clone and query `graphify-out/` instead of grepping the monorepo.

# Environments

| Machine | Use | Notes |
|---|---|---|
| **Work laptop (Axis)** | Planning, research, docs only | No Docker/WSL installs, no running LearnHouse, no real API keys. Avoid anything that could raise IT flags. |
| **DavidLab** (personal homelab, Windows + WSL2 Ubuntu) | Fork, clone, `npx learnhouse dev`, real `.env`, all development | LearnHouse clone at `~/dev/learnhouse` **inside WSL**, never in OneDrive. Real keys in `apps/api/.env` there. Existing containers (n8n, Jellyfin, cloudflared, nginx) must not be touched. |
| **Cloud Claude session** | Source reading, docs, plans, reviews | Can clone GitHub; cannot pull Docker Hub images, install pgvector, or fetch Python 3.14.7. Cannot run LearnHouse. |

Requirements on DavidLab (inside Ubuntu): Docker Desktop with WSL integration, Node 18+ (24 used), `uv`, `bun` 1.4.2, Git, `gh`. At least 4 GB RAM for the stack, 20 GB disk.

# Roadmap

- **Phase 0. Understand LearnHouse**: run it, explore the UI, map web/API/DB, course/activity models, auth, AI and RAG. Write `docs/ARCHITECTURE_NOTES.md`. No major changes.
- **Phase 1. Personal experience**: **Learning Inbox first**, then dashboard, learning domains, projects, resource library, personal notes and navigation.
- **Phase 2. Capture**: YouTube ingestion and transcripts, AI summaries, concept extraction, GitHub resources, Markdown notes, tagging.
- **Phase 3. Connected knowledge**: topics, relationships, projects/resources ↔ topics, graph view, roadmaps, better search.
- **Phase 4. Learning intelligence**: AI tutor, RAG over personal content, quizzes, active recall, spaced repetition, mastery, recommendations.
- **Phase 5. Automation**: YouTube → transcript → summary → concepts → questions → graph; repo → README → architecture → topics; finished project → skills → evidence → reflection.
- **Phase 6. Multi-user** (only once the personal version is excellent): profiles, shared paths, public courses, study groups.

# Current Priority

1. On the homelab machine: fork → clone → `npx learnhouse dev` → create a local admin → explore without modifying anything.
2. Map where courses, activities, progress, auth and AI/RAG live. Write `docs/ARCHITECTURE_NOTES.md`.
3. Design how the **Personal Learning Inbox** fits cleanly (model, migration, router, page, nav entry) and log the decision.
4. Build the Inbox end-to-end and test it. No rewrites.
5. On the homelab, also install INDEX 0 (www.index-0.in) to explore it as a reference. Never install it on the work laptop.

# Important Commands

Read from upstream source (`dev`, `5e28b07`). Phase 0 confirms them on DavidLab; mark each ✅ once it has actually run there.

```bash
# Setup (DavidLab, inside WSL Ubuntu)
gh repo fork learnhouse/learnhouse --clone=false     # creates Darideivi/learnhouse
git clone https://github.com/Darideivi/learnhouse.git ~/dev/learnhouse && cd ~/dev/learnhouse
git remote add upstream https://github.com/learnhouse/learnhouse.git
git fetch upstream && git merge upstream/dev          # upstream default branch is dev

# Run (Postgres + Redis in Docker; API :1338, web :3000, collab :4000 native, hot reload)
npx learnhouse dev            # first run is interactive: dev defaults + admin email/password
npx learnhouse status | logs | doctor | health
docker compose -f .learnhouse/docker-compose.dev.yml -p learnhouse-dev down   # stop DB + Redis

# Database (from apps/api). Fresh DBs come from create_all, not Alembic.
uv run alembic current                       # empty until stamped
uv run alembic stamp head                    # once, before the first custom migration
uv run alembic revision --autogenerate -m "add inbox_item"
uv run alembic upgrade head

# Tests and lint
cd apps/api && uv run pytest src/tests/ -q   # in-memory SQLite, no Postgres needed
cd apps/api && uvx ruff check .
cd apps/web && bun test tests
cd apps/web && bunx eslint .                 # report-only upstream
cd apps/web && bunx next typegen && bunx tsc --noEmit
scripts/lockfiles.sh                         # after touching package.json or pyproject.toml

# Code map
graphify .            # then query graphify-out/ instead of grepping
```

# Project Documentation

| File | Purpose |
|---|---|
| `LEARNHOUSE_PERSONAL_LEARNING_OS_MASTER_PLAN.md` | Detailed vision, features, phases and data model. The deep reference behind this file. Moves to `docs/MASTER_PLAN.md` in the repo. |
| `notes/` | **My live knowledge base (markdown)**: `inbox.md`, `plan.md`, `topics/`, `resources/`, `projects/`, `journal/`. Every file has YAML frontmatter (`type`, `status`, `topics`, …) designed for the app to import later. Read `notes/README.md` for the conventions. |
| `notes/resources/ai-skills-core-10.md` | Claude Code skills shortlist (reference, not rules). |
| `notes/resources/youtube-jeff-su-ai-agents-clearly-explained.md` | AI fundamentals from Jeff Su's video. Seeds the AI topics in `notes/topics/`. |
| `notes/resources/public-apis.md` | Pointer to github.com/public-apis/public-apis. Check it first when a feature or practice project needs an external API. Keys go in `.env`. |
| `info.md` | Old scratch links (now copied into `notes/inbox.md`). |
| `.env.example` | What we add to `apps/api/.env` (placeholders). Real `.env` only on DavidLab. |
| `docs/STATUS.md` | **Handoff file.** Read first, update last, every session. |
| `docs/OPEN_QUESTIONS.md` | Decisions waiting for David, each with what it blocks and a default. |
| `docs/PHASE0_PLAN.md` | Step-by-step plan for running and understanding LearnHouse on DavidLab, with ready-to-paste `/goal`s. |
| `docs/ARCHITECTURE_NOTES.md` | How LearnHouse works: request flow, data model, auth, AI/RAG, what can be hidden, migrations and tests. |
| `docs/DECISIONS.md` | Architecture decisions (accepted and proposed), org settings to apply, Phase 1 code tasks. |
| `docs/LEARNING_LOG.md` | Concepts learned while building, including infrastructure problems. |
| `graphify-out/` | Knowledge graph of the **GD Focus** ecosystem. A separate project, kept for reference; not LearnHouse. |

**First knowledge-base content (seed data).** `notes/` is the first real content the app must hold, and the first test of the Inbox → Resource → Topic flow. Build an importer for its frontmatter early.
- The Jeff Su file is a **YouTube resource**: Jeff Su, "AI Agents, Clearly Explained". It's a favorite for how clearly it explains. It seeds the topics LLM, AI Workflow, AI Agent, ReAct, Tools, RAG, MCP, Memory, Agent Skills and Multi-Agent Systems, with relationships (LLM → Workflow → Agent; RAG ⊂ Workflow; Agent uses Tools/Memory/Skills/MCP). Store the raw transcript with it once it's added.
- `ai-skills-core-10.md` is the **"AI Skills" reference collection**: 10 resources (GitHub repos), each linked to the topic Agent Skills.
Seed them when the Inbox ships. Keep my wording; AI may add structure, never replace my notes.

Still planned under `docs/`: `MASTER_PLAN.md` (move from the root), `FEATURE_IDEAS.md`.

When this file and the master plan disagree, **this file wins**. Update this file when a decision changes.
