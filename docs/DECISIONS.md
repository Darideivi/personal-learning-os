# Decisions

Architecture and process decisions for the Personal Learning OS. Newest at the bottom.

Status: **Accepted** (decided and in effect) · **Proposed** (drafted, waiting for David's OK) · **Superseded**.

---

## D-001 · Run LearnHouse in WSL2 Ubuntu on DavidLab

| | |
|---|---|
| Status | Accepted · 2026-10-02 |
| Decision | Develop and run LearnHouse inside WSL2 Ubuntu on DavidLab, with Docker Desktop's WSL integration. The clone lives at `~/dev/learnhouse`, outside OneDrive. |
| Why | `npx learnhouse dev` only containerises Postgres and Redis. API, web and collab run natively and need `uv` (Python 3.14.7), `bun` 1.4.2 and Node. Upstream tooling assumes Linux. WSL2 also doubles as Linux practice. |
| Alternatives | Native Windows (unsupported paths, shell scripts break). Everything in containers (not how upstream dev mode works). |
| Trade-offs | One more layer (WSL file system, `\\wsl$` paths). Files under OneDrive would sync `node_modules`, so the clone stays in WSL. |
| Revisit when | DavidLab moves to Linux, or upstream ships a fully containerised dev mode. |

## D-002 · Anthropic for chat, Gemini for embeddings (768 dims)

| | |
|---|---|
| Status | Accepted · 2026-10-02 |
| Decision | `LEARNHOUSE_AI_PROVIDER=anthropic`, embeddings through Google (`gemini-embedding-001`, 768 dims) via `LEARNHOUSE_GEMINI_API_KEY`. |
| Why | Anthropic has no embeddings API. Upstream's OpenAI embeddings path reuses `LEARNHOUSE_AI_API_KEY` (the Anthropic key), so Anthropic + OpenAI would need a code patch. Upstream already falls back to Google for Anthropic. The pgvector column is `Vector(768)`, which Gemini matches natively. Gemini has a free tier. |
| Alternatives | OpenAI embeddings (needs a patch). Ollama `nomic-embed-text` on the homelab (free, local, also 768 dims; see Proposed D-006). |
| Trade-offs | Note text is sent to Google for embedding. Switching embedding models later means re-embedding everything, because vectors from different models aren't comparable. |
| Revisit when | Embeddings cover personal notes (Phase 4), or Ollama is running on DavidLab. |

## D-003 · Project docs live in this repo, not upstream `docs/`

| | |
|---|---|
| Status | Accepted · 2026-10-02 |
| Decision | `ARCHITECTURE_NOTES.md`, `DECISIONS.md`, `LEARNING_LOG.md` and plans live in `Darideivi/personal-learning-os/docs/`. |
| Why | Upstream `docs/` is a Next.js documentation site. Keeping our notes out of the fork avoids merge conflicts. |
| Alternatives | A `docs/personal/` folder inside the fork. |
| Trade-offs | Two repos to keep in step. Code changes in the fork link back here for the "why". |
| Revisit when | The fork carries enough custom code that its own docs are needed. |

## D-004 · Hide features through config and org settings first

| | |
|---|---|
| Status | Accepted · 2026-10-02 (refined after source review) |
| Decision | Order of preference: (1) env flags, (2) OSS mode, (3) org settings stored in `OrganizationConfig` (feature toggles, admin toggles, menu items, signup mode), (4) upstream UI code edits, only in Phase 1 and only for what 1–3 can't reach. Never delete upstream code. |
| Why | Source review showed most of the CLAUDE.md hide list is already covered by OSS mode and org toggles (see `ARCHITECTURE_NOTES.md` §7), with no code changes. Fewer edits means easier upstream merges. |
| Alternatives | Patch navigation and pages directly (merge pain on every upstream sync). |
| Trade-offs | Org settings live in the database, not git. They need writing down (here) so a fresh install can be reconfigured. |
| Revisit when | Something that matters can't be hidden without code. |

## D-005 · Run in OSS mode (no `--ee`)

| | |
|---|---|
| Status | **Proposed** · 2026-10-02 |
| Decision | Always run `npx learnhouse dev` without `--ee`. Use only the AGPL-3.0 core. |
| Why | OSS mode blocks payments, SSO, audit logs, advanced analytics and SCORM in the backend, which matches the single-user scope. It keeps the project clear of Enterprise licensing. |
| Alternatives | `--ee` with `LEARNHOUSE_FORCE_EE=1` (dev-only licence bypass; not something to build on). |
| Trade-offs | No SSO. Entra ID login for the personal app would need its own work if ever wanted. |
| Revisit when | A needed feature turns out to be EE-only. |

## D-006 · Ollama embeddings instead of Gemini

| | |
|---|---|
| Status | **Proposed** · 2026-10-02 |
| Decision | Once Ollama runs on DavidLab, switch embeddings to `LEARNHOUSE_AI_EMBEDDING_PROVIDER=ollama` (`nomic-embed-text`, 768 dims). Keep Anthropic for chat. |
| Why | Personal notes stay on the homelab, embeddings cost nothing, and it matches the "local AI option" in CLAUDE.md. Same 768 dims, so no migration. |
| Alternatives | Stay on Gemini (D-002). |
| Trade-offs | Needs Ollama running whenever content is saved or searched. Switching requires re-indexing. Quality of local embeddings vs Gemini is unmeasured. Decide **before** much content exists, because every switch means a full re-embed. |
| Revisit when | Ollama is installed, or before the first large content import. |

## Org settings to apply after the first run

Recorded here because they live in the database (D-004). Confirm the exact screen names during Phase 0 exploration.

| Setting | Value | Hides |
|---|---|---|
| `admin_toggles.members.signup_mode` | `inviteOnly` | Public signup |
| `admin_toggles.security.allowed_auth_methods` | `["password"]` | Magic link, Google, SSO sign-in |
| `features.communities.enabled` | `false` | Communities, discussions |
| Podcasts, Boards, Playgrounds | leave off (default) | Their pages and menu links |
| `menu.items` | Courses, Library (others off) | Top menu clutter |

## Phase 1 code tasks (only if still visible after the settings above)

To be filled in during Phase 0 exploration: certificates page, hub / billing / new-organization routes, explore or marketing pages, member and invite screens.
