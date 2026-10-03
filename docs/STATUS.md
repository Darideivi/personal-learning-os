# Status

The handoff file. Every session reads it first and updates it last, so a fresh session can continue without the old chat.

**Last updated:** 2026-10-03 00:45, cloud session (Claude, Opus main; Fable for the Inbox design)

## Where we are

Everything that can be done without DavidLab is done. Phase 0 (running LearnHouse) is waiting on David's manual steps. The Inbox design is drafted and waiting for approval.

## Done

- Read upstream `learnhouse@dev` (`5e28b07`). Wrote `ARCHITECTURE_NOTES.md`, `DECISIONS.md` (D-001 to D-006), `LEARNING_LOG.md`.
- Corrected `PHASE0_PLAN.md` and added two ready-to-paste `/goal`s. Goal 1 now uses `scripts/davidlab/setup-tools.sh`.
- Fixed `.env.example`. Updated CLAUDE.md (DavidLab, AI choices, commands, model routing, working unattended).
- `scripts/davidlab/setup-tools.sh` and `backup-db.sh` (syntax-checked, **not yet run**).
- `docs/INBOX_DESIGN.md` drafted on Fable; key claims spot-checked against upstream source. Only upstream edit it needs: one `include_router` in `apps/api/src/router.py`.
- David answered Q1, Q2, Q5, Q9: new models (D-007), Ollama embeddings from the first run (D-006), database is the source of truth after a one-way import (D-008), Pro plan (Fable spends only usage credits). Plans and `.env.example` switched from Gemini to Ollama.

## Next

1. **David, by hand:** PHASE0_PLAN section A (WSL Ubuntu, Docker WSL integration, Ollama inside WSL + `ollama pull nomic-embed-text`) and the sudo apt line (includes `unzip`).
2. **DavidLab, Claude Code on Sonnet, auto mode:** goal 1 from PHASE0_PLAN. Then David pastes keys and runs the first `npx learnhouse dev`. Then goal 2.
3. **David:** approve `docs/INBOX_DESIGN.md` (OPEN_QUESTIONS Q10, plus its I-1 to I-7). Q3, Q4, Q6, Q8 can wait.
4. After approval and Phase 0: build the Inbox (start.md Prompt 2) on Sonnet, with one Fable review at the end.

## Blockers

- Cloud sessions can't run LearnHouse (Docker Hub, apt and the Python 3.14.7 download are blocked). Nothing more can move here until Phase 0 runs on DavidLab or David answers the open questions.

## Notes for the next session

- Credit: a Fable job interrupted mid-run on 2026-10-03 spent credit without producing output. Don't interrupt Fable jobs; resume them with SendMessage instead of restarting.
- Push access to this repo works (Claude GitHub App installed 2026-10-03).
