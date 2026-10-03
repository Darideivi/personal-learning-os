# Feature Ideas

Parking lot. **Nothing here is approved or scheduled.** An idea moves to the roadmap only if it strengthens the core loop (CAPTURE → LEARN → UNDERSTAND → BUILD → DOCUMENT → CONNECT → REVIEW → REMEMBER) and improves one of: Capture, Understanding, Connection, Practice, Progress, Application, Retention, Retrieval. Roadmap lives in `CLAUDE.md`; detail in `MASTER_PLAN.md`.

Format: idea · loop step · phase it would fit · cost note.

## Capture
- **Share-sheet / browser bookmarklet to the Inbox** · Capture · after Inbox v1 · one authenticated `POST /inbox/`, no new model.
- **Telegram or n8n webhook into the Inbox** · Capture · Phase 2 · n8n already runs on DavidLab; needs an API token path (Inbox v1 is session-only).
- **Command capture** (`type=command`) with a one-line cheat-sheet view · Capture/Retrieval · Phase 1.

## Understanding and retention
- **Coach-style hints** (escalating hints, full answer last) · Understanding · Phase 4 · borrowed idea from INDEX 0.
- **Questions generated from my own notes**, always editable · Retention · Phase 4.
- **"Explain it back" box per topic**: my explanation outranks the AI summary and counts as evidence · Understanding/Progress · Phase 3.

## Connection and retrieval
- **Backlinks on topic pages** (what resources, projects and notes mention this topic) · Connection · Phase 3 · plain SQL joins.
- **Search box across everything** with a topic filter · Retrieval · Phase 3 · start with Postgres full-text, add pgvector later.
- **Notes export back to markdown** · Retrieval/safety · needed because of D-008 (database is the source of truth).

## Review and progress
- **Sunday review screen**: empty the Inbox, update topic status, write the journal entry in one flow · Review · Phase 1–3.
- **Weak-topic detection** from review results and age since last use · Retention · Phase 4.
- **Evidence ledger per topic** (watched < quiz < lab < explanation < review < project) · Progress · Phase 3–4 (Q4).

## Operations
- **Nightly `pg_dump` + restore test** (`scripts/davidlab/backup-db.sh`) · safety · before the first real import (Q7).
- **Ollama for everyday summaries**, Anthropic for heavy tasks · cost · Phase 2.

## Rejected for now
- Separate graph or vector database (CLAUDE.md: one Postgres).
- Streaks, badges, XP (vanity progress; against the principles).
- Multi-user features before the personal version is excellent (Phase 6).
