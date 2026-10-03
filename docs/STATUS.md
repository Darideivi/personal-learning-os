# Status

The handoff file. Every session reads it first and updates it last, so a fresh session can continue without the old chat.

**Last updated:** 2026-10-03, cloud session (Claude, Sonnet, Inbox build)

## Where we are

LearnHouse **runs on DavidLab** (web :3000, API :1338, collab :4000, DB + Redis healthy). Phase 0 checks are done except the ones that need a browser or the Anthropic key. The **Inbox design is APPROVED** (Q10, 2026-10-03, with four amendments); the Inbox build is the next code session.

## Inbox build (cloud session, 2026-10-03): written, NOT verified

Branch `feat/learning-inbox` in `Darideivi/learnhouse`, cut from `dev` (`5e28b07`). Last commit: `75771f7` (after the Fable review: PATCH can clear `url`, tab test ids so the E2E selector is unambiguous, unused prop removed). Pushed to the fork only; no PR. The only edit to an existing upstream file is `apps/api/src/router.py` (one import and one `include_router`).

**Nothing was run** except one thing: the `detect_type` logic and its 13 test cases were checked in isolation under the sandbox's Python 3.11 (13/13 matched), outside pytest. No pytest, Alembic, ruff, tsc or Playwright run happened here. All of it needs DavidLab.

| # | Deliverable | Built |
|---|---|---|
| 1 | `src/db/inbox/inbox_items.py` | `InboxItem`, `InboxItemType`/`InboxItemStatus`, Create/Update/Read, composite index, `inbox_` uuid, str dates, `source`, `reviewed_date`. Validators for URL (http/https), blank text/title, length limits. |
| 2 | `src/services/inbox/inbox.py` | create, list (status, paging, newest first), get, patch (sets/clears `reviewed_date`), delete, `detect_type()`. Every query filters on `user_id`; `require_org_membership(resolve_acting_user_id(...))` on create and list. |
| 3 | `src/routers/inbox/inbox.py` + `router.py` | Five routes, mounted at `/inbox` with `require_authenticated_user`. |
| 4 | Tests | `test_inbox_router.py` (cases 1-9 incl. unpatched `other_org` 403) and `test_inbox_detect_type.py` (parametrized). |
| 5 | Web | `services/inbox/inbox.ts`, `inbox/page.tsx`, `InboxClient.tsx`, `inbox-list.tsx`. No upstream UI edits, no new deps. |
| 6 | E2E | `apps/e2e/features/inbox/tests/capture.spec.ts`; uses `ADMIN_STATE` from global-setup, so credentials come only from env vars. |
| 7 | Migration | `e7a1c4d9b2f0_add_inbox_item.py`, `down_revision = b1c2d3e4f5a6` (single head, found by following the chain). Idempotent guard; downgrade drops table and both enum types. |

Fable review (read-only, nothing run): no blocking findings. Run-time risk for step e is Q17. Differences from the design (details in LEARNING_LOG): enum labels in Postgres are member NAMES (`YOUTUBE`, `OPEN`), not values; the shared `RequestBodyWithAuthHeader` drops the body for PATCH, so `updateInboxItem` builds its own request; the Archive filter is only reachable through the All tab (tabs are Open/Reviewed/All as specified); 

### Also done in the cloud (same session, run and passing here)

- `scripts/notes/check_notes.py` (answers Q15): 12 notes files, 0 problems.
- `scripts/notes/import_inbox.py` (start.md Prompt 3, partial): parses `notes/inbox.md` into 5 items; dry run by default. `--apply` goes through the Inbox API and has **not been run** (needs the stack, a token and the branch deployed; Q18). Environment: `LEARNHOUSE_API_URL`, `LEARNHOUSE_TOKEN`, `LEARNHOUSE_ORG_ID`.
- `scripts/notes/test_notes_scripts.py`: 8 unittest cases, all pass (`python3 scripts/notes/test_notes_scripts.py`).
- Moved the master plan to `docs/MASTER_PLAN.md` and updated CLAUDE.md.
- Not doable in the cloud, still open: Q13 key, browser click-through (Q14), the full pytest result, the checklist below, seeding Jeff Su/topics (needs Topic/Resource models), `FEATURE_IDEAS.md` (needs David's ideas).

### DavidLab verification checklist (in order)

a. **Stop the API process first** (INBOX_DESIGN §3 hot-reload trap: `create_all` would create the table). Pull the branch (`git fetch origin && git checkout feat/learning-inbox`). From `apps/api`: `uv run alembic upgrade head`; confirm table and enum types (`\d inboxitem`, `\dT inboxitemtype inboxitemstatus` in psql). Then `uv run alembic downgrade -1` and `uv run alembic upgrade head` again. If the table already exists, the migration is a no-op: drop it and both types first (INBOX_DESIGN §3) to test for real.
b. `cd apps/api && uv run pytest src/tests/routers/test_inbox_router.py src/tests/services/test_inbox_detect_type.py -q 2>&1 | tee /tmp/inbox-tests.log`
c. Restart API and web. In the browser at `/orgs/default/inbox` type "reviewed" and capture a YouTube URL; mark it reviewed.
d. Add the Inbox menu link by resending the whole menu list with the custom item (INBOX_DESIGN §6 amendment: Courses, Library, the disabled built-ins, plus `{"type":"custom","enabled":true,"order":0,"label":"Inbox","url":"/inbox","icon":"Lightbulb"}`).
e. `cd apps/e2e && E2E_BASE_URL=http://localhost:3000 E2E_ADMIN_EMAIL=admin@school.dev E2E_ADMIN_PASSWORD=<from admin-credentials.txt> bunx playwright test features/inbox`
f. Full API suite once, in the background: `cd apps/api && nohup uv run pytest src/tests/ -q > /tmp/full-api-tests.log 2>&1 &`
g. Also worth running (not in the list): `cd apps/api && uvx ruff check src/db/inbox src/services/inbox src/routers/inbox`, and `cd apps/web && bunx next typegen && bunx tsc --noEmit`.

## Done in goal 2 (2026-10-03)

- Fixed why `npx learnhouse dev` never started: Linux `node`/`bun`/`uv` weren't on the PATH (`.bashrc` early-returns when `PS1` is unset). Now `/root/.toolchain.sh` is sourced from `.profile` and the top of `.bashrc`.
- Started the stack non-interactively: pre-wrote the dev env defaults, ran `learnhouse dev --admin-email --admin-password`. Admin login `admin@school.dev`; the generated password is in `/root/dev/learnhouse/.learnhouse/admin-credentials.txt` (gitignored, never copied into this repo).
- Verification passed: `docker ps` (db + redis healthy, n8n/Jellyfin/cloudflared/nginx untouched), `curl :1338/` returns the welcome message, `:3000` returns 200, Ollama lists `nomic-embed-text`, `alembic current` showed no revision before stamping.
- `uv run alembic stamp head` run once: now `b1c2d3e4f5a6 (head)`.
- Org settings applied through the API and read back: signup `inviteOnly`, sign-in `["password"]`, communities off, menu = Courses + Library. Real stored paths are in ARCHITECTURE_NOTES section 7.
- Sections F and G docs: ARCHITECTURE_NOTES ⏳ items confirmed or marked open, DECISIONS (org settings applied), LEARNING_LOG (5 new entries), CLAUDE.md commands marked ✅ only where run, OPEN_QUESTIONS (Q11 answered; Q13 to Q15 added).

## Failing or not verified

- **`uv run pytest src/tests/ -q`**: started 2026-10-03, first run went 22+ minutes at ~95% CPU with no output (piped through `tail`), so it was stopped. 5,836 tests collect in 7 s. A second run with a log (`/root/pytest-run.log` in Ubuntu) was in progress at the end of the session; its result is **not yet recorded**.
- **AI panel / embeddings rows**: not checked. `LEARNHOUSE_AI_API_KEY` is still the placeholder (Q13).
- **Browser checks**: Chrome (Claude in Chrome) showed a connection error page for `http://localhost:3000/login` twice, although PowerShell gets 200 (Q14).
- **`python3 scripts/notes/check_notes.py`**: the file doesn't exist in this repo (Q15), so it was not run.
- Not run: `npx learnhouse status|logs|doctor|health`, web tests, ruff, eslint, tsc, `git fetch upstream`.

## Click-through list for David (browser)

1. Open http://localhost:3000 (try `http://[::1]:3000` if it won't load) and log in as `admin@school.dev`.
2. Create a course, a chapter and an activity; open the editor and confirm the collab websocket (port 4000) connects.
3. Dashboard → Organization settings: confirm the settings above show as applied and note the exact screen names (DECISIONS and ARCHITECTURE_NOTES section 7).
4. Look for what is still visible: certificates, hub/billing/new-org routes, explore pages, member and invite screens. List them as Phase 1 code tasks in DECISIONS.
5. After putting the real key in `apps/api/.env` (Q13): open the AI panel and generate text, then save an activity and check `course_embedding` rows.
6. Try library folders, search and progress (Trail).

## Next

1. **David:** Q13 (Anthropic key), then the click-through list above. After the DavidLab checklist passes, run `import_inbox.py --apply`.
2. ~~Approve the Inbox design~~ **Done 2026-10-03.** Optional: Q7 backup cron (line in the header of `scripts/davidlab/backup-db.sh`). Q3, Q4, Q6, Q8 can wait.
3. Record the pytest result here, then build the Inbox on branch `feat/learning-inbox` (start.md Prompt 2) on Sonnet, with one Fable review at the end. Follow INBOX_DESIGN §3 (stop the API before adding the model) and §8 (run only the new tests).

## Blockers

- The dev stack runs from the session that started it. If that session ends, restart with `cd ~/dev/learnhouse && npx learnhouse dev` in Ubuntu; it reuses the DB.
- Items under "Failing or not verified" need David (key, browser) or an answer to Q15.

## History (earlier sessions)

### Done before goal 2

- Read upstream `learnhouse@dev` (`5e28b07`). Wrote `ARCHITECTURE_NOTES.md`, `DECISIONS.md` (D-001 to D-006), `LEARNING_LOG.md`.
- Corrected `PHASE0_PLAN.md` and added two ready-to-paste `/goal`s. Goal 1 now uses `scripts/davidlab/setup-tools.sh`.
- Fixed `.env.example`. Updated CLAUDE.md (DavidLab, AI choices, commands, model routing, working unattended).
- `scripts/davidlab/setup-tools.sh` and `backup-db.sh` (syntax-checked, **not yet run**).
- `docs/INBOX_DESIGN.md` drafted on Fable; key claims spot-checked against upstream source. Only upstream edit it needs: one `include_router` in `apps/api/src/router.py`.
- David answered Q1, Q2, Q5, Q9: new models (D-007), Ollama embeddings from the first run (D-006), database is the source of truth after a one-way import (D-008), Pro plan (Fable spends only usage credits). Plans and `.env.example` switched from Gemini to Ollama.

### Done on DavidLab (goal 1, 2026-10-03, Sonnet)

- `setup-tools.sh` ran in WSL Ubuntu: node v24.21.0, npm 11.19.0, bun 1.4.2, uv 0.12.22, graphify 0.9.74. Two fixes: shell scripts had CRLF endings (added `.gitattributes` with `*.sh text eol=lf`, converted both scripts), and the Docker check is now a warning instead of a hard stop (tools don't need Docker).
- Forked `Darideivi/learnhouse` and cloned it to `/root/dev/learnhouse` inside WSL. `git remote -v` shows origin = Darideivi/learnhouse, upstream = learnhouse/learnhouse.
- `apps/api/.env` created with the D.1 block, placeholders only (`LEARNHOUSE_AI_API_KEY=<anthropic-key>`). It is gitignored. Ollama and `nomic-embed-text` were already present in Ubuntu.
- Nothing committed or pushed. Existing containers untouched. `npx learnhouse dev` not run.

### Old Next list (before goal 2, superseded)

1. **David, by hand:** enable Docker WSL integration for Ubuntu (OPEN_QUESTIONS Q11). Without it `npx learnhouse dev` can't start Postgres/Redis.
2. **David:** open `apps/api/.env` (`! wsl -d Ubuntu nano ~/dev/learnhouse/apps/api/.env`), replace `<anthropic-key>` with the real key, then in his own Ubuntu terminal run `cd ~/dev/learnhouse && npx learnhouse dev` (answer yes to dev defaults, set admin email/password) and leave it running. First run takes several minutes.
3. **Then** run goal 2 from PHASE0_PLAN on Sonnet in auto mode.
4. Commit the `.gitattributes` + script fixes in this repo when David says so (currently uncommitted).
3. **David:** approve `docs/INBOX_DESIGN.md` (OPEN_QUESTIONS Q10, plus its I-1 to I-7). Q3, Q4, Q6, Q8 can wait.
4. After approval and Phase 0: build the Inbox (start.md Prompt 2) on Sonnet, with one Fable review at the end.

### Old Blockers (before goal 2, superseded)

- Cloud sessions can't run LearnHouse (Docker Hub, apt and the Python 3.14.7 download are blocked). Nothing more can move here until Phase 0 runs on DavidLab or David answers the open questions.

### Notes for the next session

- Credit: a Fable job interrupted mid-run on 2026-10-03 spent credit without producing output. Don't interrupt Fable jobs; resume them with SendMessage instead of restarting.
- Push access to this repo works (Claude GitHub App installed 2026-10-03).
