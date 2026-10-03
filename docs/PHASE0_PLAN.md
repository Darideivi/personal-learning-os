# Phase 0 Plan — Run LearnHouse on the homelab and understand it

Written 2026-10-02 after reading every file in this repo and verifying upstream `learnhouse/learnhouse` (branch `dev`) via the GitHub API. Decisions below were confirmed with David in that session.

## How to use this file

Paste into a new Claude Code session **running on the homelab machine (DavidLab)**:

```text
Read CLAUDE.md and docs/PHASE0_PLAN.md. Follow the plan step by step. Use ECC. Ask me before anything in section A, and stop when section G is done.
```

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
| CLI writes three env files with generated secrets: `apps/api/.env` (`LEARNHOUSE_AUTH_JWT_SECRET_KEY`, `COLLAB_INTERNAL_KEY`), `apps/web/.env.local` (`NEXT_PUBLIC_LEARNHOUSE_BACKEND_URL=http://localhost:1338/`), `apps/collab/.env` (port 4000, API URL, same JWT + internal key). All gitignored. | `apps/cli/src/services/env-check.ts` |
| Everything else falls back to `apps/api/config/config.yaml`: tenancy single, port 1338, domain `localhost:3000`, AI off, provider google, Postgres/Redis on localhost. **Env vars override yaml.** | `config.yaml`, `config.py` |
| Flags: `LEARNHOUSE_SAAS`, `LEARNHOUSE_USE_DEFAULT_ORG`, `LEARNHOUSE_DEVELOPMENT_MODE`, `LEARNHOUSE_IS_AI_ENABLED`, `LEARNHOUSE_AI_PROVIDER`, `LEARNHOUSE_AI_API_KEY`, `LEARNHOUSE_AI_MODEL_FAST/STANDARD/PRO`, `LEARNHOUSE_AI_EMBEDDING_PROVIDER/MODEL/DIMENSIONS`, `LEARNHOUSE_GEMINI_API_KEY`; web `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG`. | `config.py`, `apps/cli/src/templates/env.ts` |
| Embeddings are pinned to **768 dimensions** (`Vector(768)` column). Changing it needs an Alembic migration. `.env.example` in this repo wrongly says 1536. | `apps/api/src/services/ai/llm/embeddings.py`, `src/db/course_embeddings.py` |
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
- Optional, only if smooth: `uv tool install graphifyy` for the code map. `ecc:codebase-onboarding` alone is enough.
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

1. `cd ~/dev/learnhouse && npx learnhouse dev --admin-email dpena1997@hotmail.com --admin-password <David chooses>` in the background. First run installs dependencies (several minutes).
2. Once the CLI has written `apps/api/.env`, append the AI config with **placeholders**. David then pastes the real keys himself with `! wsl -d Ubuntu nano ~/dev/learnhouse/apps/api/.env` so keys never pass through chat:
   ```bash
   LEARNHOUSE_DEVELOPMENT_MODE=true
   LEARNHOUSE_SAAS=false
   LEARNHOUSE_USE_DEFAULT_ORG=true
   LEARNHOUSE_IS_AI_ENABLED=true
   LEARNHOUSE_AI_PROVIDER=anthropic
   LEARNHOUSE_AI_API_KEY=<anthropic-key>
   LEARNHOUSE_AI_MODEL_FAST=claude-haiku-4-5
   LEARNHOUSE_AI_MODEL_STANDARD=claude-sonnet-5-5
   LEARNHOUSE_AI_MODEL_PRO=claude-opus-5-5
   LEARNHOUSE_AI_EMBEDDING_PROVIDER=google
   LEARNHOUSE_GEMINI_API_KEY=<gemini-key>
   ```
   Verify the Anthropic model ids with the `claude-api` skill before writing them. Restart the API (`ra` key in the dev console, or rerun).
3. Ensure `apps/web/.env.local` has `NEXT_PUBLIC_LEARNHOUSE_MULTI_ORG=False`.

### E. Hide what I don't need (config only, no upstream code edits)

Payments/Stripe, email, Tinybird, Sentry: leave their vars unset. SaaS off, default org on, multi-org off. While exploring, list which nav/UI items still appear (marketplace, certificates, pricing, members/invites, signup) and record them in `docs/DECISIONS.md` as **Phase 1 code tasks**. Do not edit upstream UI in Phase 0.

### F. Explore and document

- As admin: create one course → chapter → activity, open the Tiptap editor, try the AI panel, collections, search, progress.
- Run `ecc:codebase-onboarding` on `~/dev/learnhouse` (plus graphify if installed).
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
- `cd apps/api && uv run alembic current` and `uv run pytest -x -q` run (confirm the exact invocation and record it in CLAUDE.md).
- All documents in F and G exist, and CLAUDE.md's commands are the ones actually used.

## Out of scope for Phase 0

Inbox (design or code), nav/UI edits in upstream code, pushing to the fork, INDEX 0 install, Playwright/Serena/Spec Kit, exposing LearnHouse through the Cloudflare tunnel.

## Next session (Phase 1 start)

`start.md` Prompt 2: design the Learning Inbox (SQLModel `InboxItem`, Alembic migration, FastAPI router, `/inbox` page, nav entry) with `/ecc:plan`, wait for approval, then build with tests on branch `feat/learning-inbox`.
