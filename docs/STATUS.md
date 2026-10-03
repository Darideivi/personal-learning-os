# Status

The handoff file. Every session reads it first and updates it last, so a fresh session can continue without the old chat.

**Last updated:** 2026-10-02, cloud session (Claude, Opus)

## Where we are

Phase 0 prep is done from source reading. The LearnHouse run itself hasn't started.

## Done

- Read upstream `learnhouse@dev` (`5e28b07`). Drafted `ARCHITECTURE_NOTES.md`, `DECISIONS.md` (D-001 to D-006), `LEARNING_LOG.md`.
- Corrected `PHASE0_PLAN.md` (interactive first run, AI config before first run, org settings instead of code, Alembic expectations).
- Fixed `.env.example` (Gemini, 768 dims). Updated CLAUDE.md (DavidLab, AI choices, commands, model routing, working unattended).
- Parked 9 decisions in `OPEN_QUESTIONS.md`.

## Next

1. **David:** PHASE0_PLAN section A by hand (WSL Ubuntu, Docker WSL integration, Gemini key).
2. **DavidLab session on Sonnet:** run PHASE0_PLAN B–G with the `/goal` in that file.
3. **Short Fable session:** answer `OPEN_QUESTIONS.md` Q1–Q5, turn answers into DECISIONS entries.
4. Inbox design (`start.md` Prompt 2), on Fable.

## Blockers

- Claude can't push to `Darideivi/personal-learning-os` until the Claude GitHub App is installed on it. Until then, cloud-session changes reach the repo only as patches David applies.
- Cloud sessions can't run LearnHouse (Docker Hub, apt and the Python 3.14.7 download are blocked).
