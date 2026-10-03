# Open Questions

Decisions only David can make. Claude parks questions here instead of stopping, and keeps working on whatever doesn't depend on them.

How to answer: write the answer under the question (a line is enough), then move it to **Answered** with the date. The next session turns it into a `docs/DECISIONS.md` entry.

| Field | Meaning |
|---|---|
| Blocks | What work waits on the answer |
| Default | What Claude will assume if no answer arrives before that work starts |

---

## Waiting for David

### Q3 · Is a saved YouTube video a course activity or a standalone Resource?
Upstream already has `SUBTYPE_VIDEO_YOUTUBE` activities inside courses.
- **Blocks:** Phase 2 YouTube ingestion
- **Default:** Standalone Resource that can link to many topics.

### Q4 · Topic mastery: on top of Trail, or separate tables?
Trail only tracks completion.
- **Blocks:** Phase 3–4 progress design
- **Default:** Separate tables that read Trail as one source of evidence.

### Q6 · Fork tracks upstream `dev` or release tags? How often to merge?
- **Blocks:** first upstream sync
- **Default:** Track `dev`, merge every 2 weeks on a branch, run tests before merging.

### Q7 · Backup plan for the Postgres volume on DavidLab?
- **Blocks:** first real content import
- **Default:** Nightly `pg_dump` with `scripts/davidlab/backup-db.sh` (keeps 14, written 2026-10-03, untested). Add the crontab line from its header once LearnHouse runs.

### Q8 · Keep `graphify-out/` (GD Focus graph) in this repo?
It maps a different project and was built from the work laptop.
- **Blocks:** nothing
- **Default:** Leave it until David decides.

### Q10 · Approve the Inbox design draft?
`docs/INBOX_DESIGN.md` (written on Fable, assumes the Q1 and Q5 defaults). Its own open decisions I-1 to I-7 are listed at the end of that file.
- **Blocks:** Inbox build (start.md Prompt 2)
- **Default:** none. The build waits for David's OK, because it's real code in the fork.

## Answered

### Q1 · Where does personal knowledge live: inside LearnHouse courses, or in new models?
**Answer (2026-10-03):** New models. Recorded as D-007.

### Q2 · Gemini or Ollama for embeddings?
**Answer (2026-10-03):** Ollama on DavidLab from the first run. Recorded as D-006 (accepted).

### Q5 · Source of truth once the app exists: `notes/` markdown or the database?
**Answer (2026-10-03):** App database, after a one-way import. Recorded as D-008.

### Q9 · Which Claude plan are you on?
**Answer (2026-10-03):** Pro. Fable runs only on usage credits, so Fable work is exactly what spends the $100 credit; Opus/Sonnet/Haiku use the plan limits.

