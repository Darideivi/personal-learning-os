# Open Questions

Decisions only David can make. Claude parks questions here instead of stopping, and keeps working on whatever doesn't depend on them.

How to answer: write the answer under the question (a line is enough), then move it to **Answered** with the date. The next session turns it into a `docs/DECISIONS.md` entry.

| Field | Meaning |
|---|---|
| Blocks | What work waits on the answer |
| Default | What Claude will assume if no answer arrives before that work starts |

---

## Waiting for David

### Q1 · Where does personal knowledge live: inside LearnHouse courses, or in new models?
Upstream RAG only covers courses (`CourseEmbedding.course_id` is required). Notes, videos and projects as courses/activities get RAG for free; new models (`InboxItem`, `Resource`, `Topic`) need their own embedding table.
- **Blocks:** Inbox design (Phase 1)
- **Default:** New models for Inbox/Resource/Topic, plus a separate embedding table designed in Phase 4. Courses stay courses.

### Q2 · Gemini or Ollama for embeddings?
Gemini sends note text to Google. Ollama keeps it on DavidLab, also 768 dims. Every switch later means re-embedding everything.
- **Blocks:** first real content import
- **Default:** Gemini for Phase 0 testing only; decide before importing `notes/`.

### Q3 · Is a saved YouTube video a course activity or a standalone Resource?
Upstream already has `SUBTYPE_VIDEO_YOUTUBE` activities inside courses.
- **Blocks:** Phase 2 YouTube ingestion
- **Default:** Standalone Resource that can link to many topics.

### Q4 · Topic mastery: on top of Trail, or separate tables?
Trail only tracks completion.
- **Blocks:** Phase 3–4 progress design
- **Default:** Separate tables that read Trail as one source of evidence.

### Q5 · Source of truth once the app exists: `notes/` markdown or the database?
Two-way sync is a trap.
- **Blocks:** notes importer (start.md Prompt 3)
- **Default:** One-way import now (markdown → app). The database becomes the source of truth after import.

### Q6 · Fork tracks upstream `dev` or release tags? How often to merge?
- **Blocks:** first upstream sync
- **Default:** Track `dev`, merge every 2 weeks on a branch, run tests before merging.

### Q7 · Backup plan for the Postgres volume on DavidLab?
- **Blocks:** first real content import
- **Default:** Nightly `pg_dump` to a folder outside Docker; Claude proposes the script after Phase 0.

### Q8 · Keep `graphify-out/` (GD Focus graph) in this repo?
It maps a different project and was built from the work laptop.
- **Blocks:** nothing
- **Default:** Leave it until David decides.

### Q9 · Which Claude plan are you on?
On Pro, Fable runs only on usage credits. On Max, it uses weekly limits first, then credits.
- **Blocks:** knowing whether the $100 credit is what Fable spends
- **Default:** Follow the model routing in CLAUDE.md either way.

## Answered

_(none yet)_
