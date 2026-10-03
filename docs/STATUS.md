# Status

The handoff file. Every session reads it first and updates it last, so a fresh session can continue without the old chat.

**Last updated:** 2026-10-03, DavidLab session (Claude, Sonnet, goal 1)

## Where we are

Everything that can be done without DavidLab is done. Phase 0 (running LearnHouse) is waiting on David's manual steps. The Inbox design is drafted and waiting for approval.

## Done

- Read upstream `learnhouse@dev` (`5e28b07`). Wrote `ARCHITECTURE_NOTES.md`, `DECISIONS.md` (D-001 to D-006), `LEARNING_LOG.md`.
- Corrected `PHASE0_PLAN.md` and added two ready-to-paste `/goal`s. Goal 1 now uses `scripts/davidlab/setup-tools.sh`.
- Fixed `.env.example`. Updated CLAUDE.md (DavidLab, AI choices, commands, model routing, working unattended).
- `scripts/davidlab/setup-tools.sh` and `backup-db.sh` (syntax-checked, **not yet run**).
- `docs/INBOX_DESIGN.md` drafted on Fable; key claims spot-checked against upstream source. Only upstream edit it needs: one `include_router` in `apps/api/src/router.py`.
- David answered Q1, Q2, Q5, Q9: new models (D-007), Ollama embeddings from the first run (D-006), database is the source of truth after a one-way import (D-008), Pro plan (Fable spends only usage credits). Plans and `.env.example` switched from Gemini to Ollama.

## Done on DavidLab (goal 1, 2026-10-03, Sonnet)

- `setup-tools.sh` ran in WSL Ubuntu: node v24.21.0, npm 11.19.0, bun 1.4.2, uv 0.12.22, graphify 0.9.74. Two fixes: shell scripts had CRLF endings (added `.gitattributes` with `*.sh text eol=lf`, converted both scripts), and the Docker check is now a warning instead of a hard stop (tools don't need Docker).
- Forked `Darideivi/learnhouse` and cloned it to `/root/dev/learnhouse` inside WSL. `git remote -v` shows origin = Darideivi/learnhouse, upstream = learnhouse/learnhouse.
- `apps/api/.env` created with the D.1 block, placeholders only (`LEARNHOUSE_AI_API_KEY=<anthropic-key>`). It is gitignored. Ollama and `nomic-embed-text` were already present in Ubuntu.
- Nothing committed or pushed. Existing containers untouched. `npx learnhouse dev` not run.

## Next

1. **David, by hand:** enable Docker WSL integration for Ubuntu (OPEN_QUESTIONS Q11). Without it `npx learnhouse dev` can't start Postgres/Redis.
2. **David:** open `apps/api/.env` (`! wsl -d Ubuntu nano ~/dev/learnhouse/apps/api/.env`), replace `<anthropic-key>` with the real key, then in his own Ubuntu terminal run `cd ~/dev/learnhouse && npx learnhouse dev` (answer yes to dev defaults, set admin email/password) and leave it running. First run takes several minutes.
3. **Then** run goal 2 from PHASE0_PLAN on Sonnet in auto mode.
4. Commit the `.gitattributes` + script fixes in this repo when David says so (currently uncommitted).
3. **David:** approve `docs/INBOX_DESIGN.md` (OPEN_QUESTIONS Q10, plus its I-1 to I-7). Q3, Q4, Q6, Q8 can wait.
4. After approval and Phase 0: build the Inbox (start.md Prompt 2) on Sonnet, with one Fable review at the end.

## Blockers

- Cloud sessions can't run LearnHouse (Docker Hub, apt and the Python 3.14.7 download are blocked). Nothing more can move here until Phase 0 runs on DavidLab or David answers the open questions.

## Notes for the next session

- Credit: a Fable job interrupted mid-run on 2026-10-03 spent credit without producing output. Don't interrupt Fable jobs; resume them with SendMessage instead of restarting.
- Push access to this repo works (Claude GitHub App installed 2026-10-03).
