# Phase 0 Plan — Run LearnHouse on the homelab and understand it

Written 2026-10-02 after reading every file in this repo and verifying upstream `learnhouse/learnhouse` (branch `dev`) via the GitHub API. Decisions below were confirmed with David in that session.

**Updated 2026-10-02 (cloud session, source review of `learnhouse@dev` `5e28b07`).** Corrections: the first `npx learnhouse dev` is interactive, so David runs it himself; AI config is written before the first run; `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG` dropped (ignored upstream); hiding is mostly org settings; Alembic expectations fixed; Haiku model id. Drafts of `ARCHITECTURE_NOTES.md`, `DECISIONS.md` and `LEARNING_LOG.md` already exist from source reading: section F **confirms and completes** them rather than starting from scratch.

## How to use this file

Run this session on **Sonnet** (`/model sonnet`): it's installs, logs and docs, so Fable credit would be wasted (see "Model routing" in CLAUDE.md). Paste into a new Claude Code session **running on the homelab machine (DavidLab)**:

```text
Read CLAUDE.md and docs/PHASE0_PLAN.md. Follow the plan step by step. Use ECC. Ask me before anything in section A, and stop when section G is done.
```

### Unattended version (two `/goal`s)

Turn on auto mode first, so goal turns don't stop for approvals. The run splits in two because the first `npx learnhouse dev` needs David at the keyboard.

**Before goal 1, David does by hand:** section A, plus `sudo apt update && sudo apt install -y git curl build-essential` inside Ubuntu (it needs his password).

**Goal 1: tools, fork and env file**

```text
/goal Following CLAUDE.md and docs/PHASE0_PLAN.md: section B tools (nvm + Node 24, bun, uv, graphifyy) work inside WSL Ubuntu, shown by printing their versions; section C is done, shown by `git -C ~/dev/learnhouse remote -v` listing origin Darideivi/learnhouse and upstream learnhouse/learnhouse; ~/dev/learnhouse/apps/api/.env exists with the D.1 block using placeholders only, never real keys. Do not run `npx learnhouse dev`. Anything that needs David goes into docs/OPEN_QUESTIONS.md, and docs/STATUS.md says what David must do next. Do not touch existing containers. Stop after 25 turns.
```

**Between the goals, David does by hand:** paste the real keys into `apps/api/.env`, then run `cd ~/dev/learnhouse && npx learnhouse dev` once in his own terminal (answer the two prompts) and leave it running.

**Goal 2: verify, hide, explore, document**

```text
/goal Following CLAUDE.md and docs/PHASE0_PLAN.md with LearnHouse already running: every check under "Verification" is shown passing in this conversation, or recorded as failing with its error in docs/LEARNING_LOG.md; org settings from docs/DECISIONS.md are applied or listed as manual steps for David; sections F and G are done (ARCHITECTURE_NOTES ⏳ items confirmed or marked open, DECISIONS and LEARNING_LOG updated, CLAUDE.md commands marked ✅ when actually run); docs/STATUS.md is updated. No upstream code edits, no commits or pushes, no real keys in any file in this repo. Decisions go to docs/OPEN_QUESTIONS.md. Stop after 40 turns.
```

Browser checks (log in, open the editor, AI panel) need Chrome on DavidLab. If the session can't drive a browser, Claude lists them in `STATUS.md` for David to click through.

**Important:** steps B–F need this machine's WSL2, Docker Desktop and browser. A cloud Claude Code sandbox cannot run them. Use the terminal/desktop app on DavidLab, or the cloud session with Remote Control connected to DavidLab. The cloud sandbox can still do section G (docs edits in this repo) and review the plan.

## Context

The Personal Learning OS is a fork of LearnHouse that will become a capture → connect → review knowledge system. Nothing has been built yet: this repo holds the plan, CLAUDE.md and the markdown knowledge base (`notes/`). `start.md` Prompt 1 defines this phase: **run LearnHouse locally, trimmed for one user, and document it. No custom features.**

### This machine (verified 2026-10-02)

| Item | Value |
|---|---|
| Hostname | DavidLab (the homelab). The "work laptop, no Docker" rule in CLAUDE.md does not apply here. |
| Hardware | i5-6500T, 15.7 GB RAM, 411 GB free on C: |
| Docker | Docker Desktop 29.8, Compose v5.5, WSL2 backend. Only the `docker-desktop` distro exists, **no Ubuntu yet**. |
| Running containers | n8n (5678), cloudflared, Jellyfin (8096), nginx (8080), nginxWithVolume (8081). Do not touch. See `~/docker/n8n/HANDOFF.md`. |
| Free ports LearnHouse needs | 3000, 1338, 4000, 5432, 6379 — all free |
| Installed | Node 24.19, npm 11, Git, gh 2.102 (authed as Darideivi) |
| **Missing** | Python, `uv`, `bun`, WSL Ubuntu |
| Repo location | This repo is in OneDrive. The LearnHouse clone must **not** be (node_modules + OneDrive sync = pain). |
| Fork | `Darideivi/learnhouse` does **not** exist yet |

### Decisions made with David

1. **Runtime: WSL2 Ubuntu.** `npx learnhouse dev` only containerises Postgres + Redis; the API, web and collab servers run natively and need `uv` (Python 3.14.7 pinned), `bun` 1.4.2 and Node. Upstream assumes Linux (shell scripts, lockfile tooling). WSL2 also doubles as the Linux curriculum.
2. **AI: Anthropic for chat, Gemini for embeddings.** CLAUDE.md said "Anthropic + OpenAI embeddings", but upstream's OpenAI embeddings path reuses the single `LEARNHOUSE_AI_API_KEY` (which would be the Anthropic key), so that combo needs a code patch. Anthropic's built-in fallback is `LEARNHOUSE_GEMINI_API_KEY`. Gemini embeddings are free-tier and natively 768-dim. David has Anthropic and OpenAI keys, **not yet a Gemini key** → get one at aistudio.google.com. Until then chat works and embeddings error.
3. **Scope: Prompt 1 only.** Inbox design is the next session.

## Verified upstream facts

| Fact | Source file in the clone |
|---|---|
| Dev compose: `pgvector/pgvector:pg16` on 5432, `redis:8.6.1-alpine` on 6379, compose project `learnhouse-dev`, written to `.learnhouse/docker-compose.dev.yml` (gitignored). Containers keep running after quit. | `apps/cli/src/commands/dev.ts` |
| Services: API `uv run python app.py` (port 1338, hot reload when `development_mode`), web `next dev --turbopack` (3000), collab `tsx watch src/index.ts` (4000). Binaries resolved from each app's `node_modules/.bin`. | `dev.ts`, `apps/api/app.py`, `apps/collab/src/index.ts` |
| Deps auto-installed on first run: `bun install` (web, collab), `uv sync` (api, downloads Python 3.14.7). | `dev.ts`, `apps/api/pyproject.toml`, `.bun-version` |
| CLI checks three env files and, after an **interactive "Apply dev defaults?" prompt**, appends only the missing vars (existing lines are kept): `apps/api/.env` (`LEARNHOUSE_AUTH_JWT_SECRET_KEY` random, `COLLAB_INTERNAL_KEY` a fixed dev default), `apps/web/.env.local` (`NEXT_PUBLIC_LEARNHOUSE_BACKEND_URL=http://localhost:1338/`), `apps/collab/.env` (port 4000, API URL, same JWT + internal key). All gitignored. | `apps/cli/src/services/env-check.ts` |
| Fresh DB schema comes from `SQLModel.metadata.create_all` at API startup, not Alembic. `alembic current` shows no revision until you `alembic stamp head`. | `src/core/events/database.py`, `apps/cli/src/commands/update.ts` |
| Web ignores `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG`; tenancy comes from the backend (`LH_tenancy` cookie). `LEARNHOUSE_TENANCY` (`single`/`multi`) supersedes `LEARNHOUSE_USE_DEFAULT_ORG`. | `apps/web/services/config/config.ts`, `config.py` |
| Without `--ee` the CLI sets `LEARNHOUSE_DISABLE_EE=1` → **OSS mode**: payments, SSO, audit logs, advanced analytics and SCORM are blocked by the backend. | `dev.ts`, `src/core/deployment_mode.py` |
| Most "hide" work is org settings (DB JSON), not code: feature toggles, admin toggles (signup mode, auth methods), menu items. | `src/db/organization_config.py` |
| **Collections were removed upstream**, replaced by Library **Folders**. | migrations `d4e5f6a7b8c9`, `7f2b9d1c3e4a` |
| Everything else falls back to `apps/api/config/config.yaml`: tenancy single, port 1338, domain `localhost:3000`, AI off, provider google, Postgres/Redis on localhost. **Env vars override yaml.** | `config.yaml`, `config.py` |
| Flags: `LEARNHOUSE_SAAS`, `LEARNHOUSE_USE_DEFAULT_ORG`, `LEARNHOUSE_DEVELOPMENT_MODE`, `LEARNHOUSE_IS_AI_ENABLED`, `LEARNHOUSE_AI_PROVIDER`, `LEARNHOUSE_AI_API_KEY`, `LEARNHOUSE_AI_MODEL_FAST/STANDARD/PRO`, `LEARNHOUSE_AI_EMBEDDING_PROVIDER/MODEL/DIMENSIONS`, `LEARNHOUSE_GEMINI_API_KEY`; web `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG`. | `config.py`, `apps/cli/src/templates/env.ts` |
| Embeddings are pinned to **768 dimensions** (`Vector(768)` column). Changing it needs an Alembic migration. `.env.example` in this repo said 1536 (fixed 2026-10-02). | `apps/api/src/services/ai/llm/embeddings.py`, `src/db/course_embeddings.py` |
| AI layer lives in `apps/api/src/services/ai/llm/{provider,embeddings,tiers,client}.py`; RAG in `src/services/ai/rag/`. Provider ids: google, openai, anthropic, deepseek, moonshot, mistral, openrouter, bedrock, ollama. | repo tree, `provider.py` |
| Admin account: `dev` prompts for email/password on first run, or accepts `--admin-email` / `--admin-password`. | `dev.ts` |
| Upstream `docs/` is a **Next.js documentation site**, not a notes folder. Our docs go in this repo's `docs/`. | repo tree |
| Lockfiles are frozen in CI: after touching `package.json` or `pyproject.toml`, run `scripts/lockfiles.sh`. | `CONTRIBUTING.md` |

## Steps

### A. David does by hand (interactive or GUI; Claude cannot)

1. In a Windows terminal: `wsl --install -d Ubuntu`. Set a UNIX username and password when prompted.
2. Docker Desktop → Settings → Resources → WSL integration → enable **Ubuntu** → Apply & restart.
3. Get a Gemini API key at aistudio.google.com (free). Have the Anthropic key handy.

Claude checks 1 and 2 with `wsl -l -v` and `wsl -d Ubuntu -- docker ps` before continuing.

### B. Tooling inside Ubuntu (Claude runs via `wsl -d Ubuntu -- bash -lc "..."`)

- `sudo apt update && sudo apt install -y git curl build-essential` — needs the sudo password, so David runs it with the `!` prefix.
- Node 24 LTS via nvm (`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash && nvm install 24`).
- `bun`: `curl -fsSL https://bun.sh/install | bash`.
- `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- `uv tool install graphifyy` for the code map. Build it once, on Sonnet, scoped to `apps/api/src`, `apps/web/app`, `apps/web/components`, `apps/web/services` (the whole monorepo is ~1,900 files and graph building costs tokens). Later sessions query `graphify-out/` instead of grepping.
- Skipped on purpose: Serena, Playwright CLI, Spec Kit. Add when Inbox work starts.

### C. Fork and clone (outside OneDrive)

- From Windows: `gh repo fork learnhouse/learnhouse --clone=false` (creates `Darideivi/learnhouse`).
- In WSL:
  ```bash
  mkdir -p ~/dev && git clone https://github.com/Darideivi/learnhouse.git ~/dev/learnhouse
  cd ~/dev/learnhouse
  git remote add upstream https://github.com/learnhouse/learnhouse.git
  git fetch upstream
  ```
- Plain https, no credential helper yet (nothing is pushed this session).
- Windows-side path for reading: `\\wsl$\Ubuntu\home\<user>\dev\learnhouse`.

### D. Run it

1. **Before the first run**, Claude creates `~/dev/learnhouse/apps/api/.env` with the AI config and **placeholders** (the CLI keeps existing lines and only appends what's missing). David pastes the real keys himself with `! wsl -d Ubuntu nano ~/dev/learnhouse/apps/api/.env`, so keys never pass through chat:
   ```bash
   LEARNHOUSE_SITE_NAME="Personal Learning OS"
   LEARNHOUSE_TENANCY=single
   LEARNHOUSE_SAAS=false
   LEARNHOUSE_IS_AI_ENABLED=true
   LEARNHOUSE_AI_PROVIDER=anthropic
   LEARNHOUSE_AI_API_KEY=<anthropic-key>
   LEARNHOUSE_AI_MODEL_FAST=claude-haiku-4-5-20251001
   LEARNHOUSE_AI_MODEL_STANDARD=claude-sonnet-5-5
   LEARNHOUSE_AI_MODEL_PRO=claude-opus-5-5
   LEARNHOUSE_AI_EMBEDDING_PROVIDER=google
   LEARNHOUSE_AI_EMBEDDING_MODEL=gemini-embedding-001
   LEARNHOUSE_AI_EMBEDDING_DIMENSIONS=768
   LEARNHOUSE_GEMINI_API_KEY=<gemini-key>
   ```
   No `LEARNHOUSE_DEVELOPMENT_MODE` (the CLI sets it) and no `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG` (web ignores it).
2. **David runs the first `npx learnhouse dev` himself** in his own Ubuntu terminal: `cd ~/dev/learnhouse && npx learnhouse dev`. It asks two interactive questions that hang if Claude runs it in the background: "Apply dev defaults?" (answer yes) and admin email + password. Typing the password at the prompt keeps it out of shell history and `ps`. First run installs dependencies (several minutes). Claude follows along with `npx learnhouse status`, `logs` and `health`.
3. After the API restarts with the keys, check the startup log for `pgvector extension not available` (should not appear) and that AI is enabled.

### E. Hide what I don't need (config only, no upstream code edits)

Payments/Stripe, email, Tinybird, Sentry: leave their vars unset. OSS mode already blocks payments, SSO, audit logs, advanced analytics and SCORM.

Then, as admin, apply the org settings listed in `docs/DECISIONS.md` ("Org settings to apply after the first run"): invite-only signup, password-only sign-in, communities off, menu trimmed to Courses + Library. These are database settings, not code, so record the exact screen path for each.

Only what is **still visible after that** (likely certificates, hub/billing/new-org routes, explore pages, member/invite screens) goes into `docs/DECISIONS.md` as **Phase 1 code tasks**. Do not edit upstream UI in Phase 0.

### F. Explore and document

- As admin: create one course → chapter → activity, open the Tiptap editor, try the AI panel, collections, search, progress.
- Read the draft `docs/ARCHITECTURE_NOTES.md` first, then use graphify and `ecc:codebase-onboarding` only to confirm the ⏳ items and fill gaps. Don't re-map what the draft already covers.
- Write `docs/ARCHITECTURE_NOTES.md` **in this repo**: web → API → DB flow; where courses/chapters/activities, progress, auth, AI/RAG, migrations and tests live; the real commands for migrations (`uv run alembic ...`), API tests (`uv run pytest`), web tests (`bun test`), lint.
- Write `docs/DECISIONS.md`: WSL2 runtime; Anthropic + Gemini embeddings and why; docs live in this repo not upstream's `docs/`; what was hidden and how; items deferred to Phase 1. Format: decision, why, alternatives, trade-offs, date, revisit-when.
- Write `docs/LEARNING_LOG.md` and update `notes/journal/2026-W40.md`: WSL2 vs Docker Desktop, env-over-yaml precedence, uv/bun lockfiles, compose project names and named volumes, the shared JWT secret between API and collab, pgvector dimension pinning, and anything that broke.

### G. Fix this repo's docs to match reality

- `CLAUDE.md`: Environments table (DavidLab is the homelab; clone lives in WSL at `~/dev/learnhouse`), AI section (Anthropic + Gemini, 768 dims), Important Commands (the ones actually run), Project Documentation table (add `docs/PHASE0_PLAN.md`, `ARCHITECTURE_NOTES.md`, `DECISIONS.md`, `LEARNING_LOG.md`).
- `.env.example`: it documents `apps/api/.env`. Drop `OPENAI_API_KEY` and 1536; add `LEARNHOUSE_GEMINI_API_KEY`, `LEARNHOUSE_AI_EMBEDDING_PROVIDER=google`, dimensions 768; note which files the CLI generates.
- `notes/projects/personal-learning-os.md`: fill `repo:` with `Darideivi/learnhouse`.
- Commit only when David asks.

## Verification

- `wsl -d Ubuntu -- docker ps` shows `learnhouse-db-dev` and `learnhouse-redis-dev` healthy; n8n, Jellyfin, cloudflared and nginx are untouched.
- `curl http://localhost:1338/` returns `{"Message":"Welcome to LearnHouse ✨"}`. `http://localhost:3000` loads from Windows.
- Log in as admin in Chrome, create a course and an activity, open the editor (collab websocket on 4000 connects).
- AI panel generates text through Anthropic. Embeddings work once the Gemini key is in.
- `cd apps/api && uv run alembic current` runs and shows **no revision** (expected: the schema came from `create_all`). Do **not** stamp yet; that's the first step of the Inbox session.
- `cd apps/api && uv run pytest src/tests/ -x -q` runs (in-memory SQLite, no Postgres needed). Record the pass/fail count.
- All documents in F and G exist, and CLAUDE.md's commands are the ones actually used.

## Out of scope for Phase 0

Inbox (design or code), nav/UI edits in upstream code, pushing to the fork, INDEX 0 install, Playwright/Serena/Spec Kit, exposing LearnHouse through the Cloudflare tunnel.

## Next session (Phase 1 start)

`start.md` Prompt 2: design the Learning Inbox (SQLModel `InboxItem`, Alembic migration, FastAPI router, `/inbox` page, nav entry) with `/ecc:plan`, wait for approval, then build with tests on branch `feat/learning-inbox`.
