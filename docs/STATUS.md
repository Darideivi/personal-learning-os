# Status

The handoff file. Every session reads it first and updates it last, so a fresh session can continue without the old chat.

**Last updated:** 2026-10-03, DavidLab session (Claude, Sonnet, goal 2)

## Where we are

LearnHouse **runs on DavidLab** (web :3000, API :1338, collab :4000, DB + Redis healthy). Phase 0 checks are done except the ones that need a browser or the Anthropic key. The **Inbox design is APPROVED** (Q10, 2026-10-03, with four amendments); the Inbox build is the next code session.

## Done in goal 2 (2026-10-03)

- Fixed why `npx learnhouse dev` never started: Linux `node`/`bun`/`uv` weren't on the PATH (`.bashrc` early-returns when `PS1` is unset). Now `/root/.toolchain.sh` is sourced from `.profile` and the top of `.bashrc`.
- Started the stack non-interactively: pre-wrote the dev env defaults, ran `learnhouse dev --admin-email --admin-password`. Admin login `admin@school.dev`; the generated password is in `/root/dev/learnhouse/.learnhouse/admin-credentials.txt` (gitignored, never copied into this repo).
- Verification passed: `docker ps` (db + redis healthy, n8n/Jellyfin/cloudflared/nginx untouched), `curl :1338/` returns the welcome message, `:3000` returns 200, Ollama lists `nomic-embed-text`, `alembic current` showed no revision before stamping.
- `uv run alembic stamp head` run once: now `b1c2d3e4f5a6 (head)`.
- Org settings applied through the API and read back: signup `inviteOnly`, sign-in `["password"]`, communities off, menu = Courses + Library. Real stored paths are in ARCHITECTURE_NOTES section 7.
- Sections F and G docs: ARCHITECTURE_NOTES ⏳ items confirmed or marked open, DECISIONS (org settings applied), LEARNING_LOG (5 new entries), CLAUDE.md commands marked ✅ only where run, OPEN_QUESTIONS (Q11 answered; Q13 to Q15 added).

## Failing or not verified

- **`uv run pytest src/tests/ -q` (run 2026-10-03, DavidLab, 24 min 29 s): 5807 passed, 15 failed, 2 errors, 21 skipped** (5,836 collected). Log: `/root/pytest-run.log` in Ubuntu. No upstream code was edited, but this is not a clean-baseline comparison (the same tests were not run on an unmodified checkout or an empty `.env`). Causes:
  - **Confirmed, environment leak:** `test_llm_provider::test_model_for_tier_defaults` expects `gemini-3.1-flash-lite` but got `claude-haiku-4-5-20251001`, because our `apps/api/.env` sets `LEARNHOUSE_AI_*` and the tests read it.
  - **Likely, same family:** 5 `test_llm_features_ollama` tests plus the boards and playgrounds stream tests: `ask_ai_stream failed: 404, model 'qwen2.5:3b' not found`. Ollama is running locally now, but only `nomic-embed-text` is pulled, and the tests expect `qwen2.5:3b`.
  - **Unconfirmed:** `test_active_users::test_ee_records` (expected HTTPException, we run OSS mode), `test_auth` and `test_security_all` stale-token naive-datetime tests, 2 `test_account_lockout_service` tests (naive `locked_until`), and 2 setup errors in `test_root_router.py`.
  - **Decision 2026-10-03 (David): low priority, not a blocker.** These are upstream tests we didn't touch, and the Inbox build runs only its own tests (INBOX_DESIGN section 8). Optional later: rerun just these 17 with the `LEARNHOUSE_*` vars cleared (`env -u` or a temporary empty `.env`) to explain the failures. Required later: after the Inbox is built, run the full suite once in the background with a log and expect the same 15 failures plus the new Inbox tests passing (5807 passed + Inbox tests). Also use these failures as the known baseline before the first upstream merge (Q6).
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

1. **David:** Q13 (Anthropic key), then the click-through list above.
2. ~~Approve the Inbox design~~ **Done 2026-10-03.** Later: Phase 1.5 "access from anywhere" (Q16). Optional: Q7 backup cron (line in the header of `scripts/davidlab/backup-db.sh`). Q3, Q4, Q6, Q8 can wait.
3. Pytest result is recorded above. Build the Inbox on branch `feat/learning-inbox` (start.md Prompt 2) on Sonnet, with one Fable review at the end. Follow INBOX_DESIGN §3 (stop the API before adding the model) and §8 (run only the new tests).

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
