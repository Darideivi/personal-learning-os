# Open Questions

Decisions only David can make. Claude parks questions here instead of stopping, and keeps working on whatever doesn't depend on them.

How to answer: write the answer under the question (a line is enough), then move it to **Answered** with the date. The next session turns it into a `docs/DECISIONS.md` entry.

| Field | Meaning |
|---|---|
| Blocks | What work waits on the answer |
| Default | What Claude will assume if no answer arrives before that work starts |

---

## Waiting for David

### Q13 · Put the real Anthropic key into `apps/api/.env`
Found 2026-10-03: `LEARNHOUSE_AI_API_KEY` is still the `<anthropic-key>` placeholder, so the AI panel cannot be verified. Claude never enters real keys. Edit the file yourself (`wsl -d Ubuntu -u root -- nano /root/dev/learnhouse/apps/api/.env`), then type `ra` in the dev window (or restart `npx learnhouse dev`) to restart the API.
- **Blocks:** Verification item "AI panel generates text through Anthropic" and the `course_embedding` row check
- **Default:** none. Needs David.

### Q14 · Click-through checks (browser) and Chrome cannot open localhost:3000
Found 2026-10-03: the Claude-in-Chrome tab showed a connection error page for `http://localhost:3000/login` twice, while PowerShell gets HTTP 200 from the same URL (and `127.0.0.1:3000` refuses, so WSL localhost forwarding is IPv6 or `localhost` only). The click-through list is in STATUS.md. If your own Chrome also fails, try `http://[::1]:3000` and tell me.
- **Blocks:** browser verification items
- **Default:** none.

### Q15 · `scripts/notes/check_notes.py` is missing
The goal says `python3 scripts/notes/check_notes.py` should still pass, but that file is not in this repo (`scripts/` only has `davidlab/`; it is not tracked in git and CLAUDE.md never mentions it). Was it on another branch, the work laptop, or the cloud session? Also, Windows has no Python, so it would have to run inside Ubuntu.
- **Blocks:** nothing
- **Default:** skip the check and record it as not run.

### Q16 · Inbox: let PATCH clear `url`, and show Archived items?
Found 2026-10-03 during the Inbox build. v1 ignores `null` in PATCH, so a `url` cannot be removed once set, and archived items only show in the All tab (tabs are Open / Reviewed / All as specified).
- **Blocks:** nothing
- **Default:** Leave as is for v1; revisit when the weekly review flow is built.

### Q12 · Ubuntu has only `root` and no normal user. Create one?
Found 2026-10-03: `wsl -d Ubuntu` logs in as `root` (home `/root`), so the clone is at `/root/dev/learnhouse` and the tools are under `/root`. Everything works, but running dev servers and Docker as root is poor Linux practice, and `~/dev` is not under a normal `/home/<name>`. Re-doing it later means re-running `setup-tools.sh` and re-cloning.
- **Blocks:** nothing now
- **Default:** Keep root for Phase 0, since it already works. Revisit if file-permission or Docker-socket problems appear.

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

## Answered

### Q10 · Approve the Inbox design draft?
**Answer (2026-10-03):** Approved with four amendments (migration hot-reload trap, run only the new tests while building, URL and length validation, E2E env vars; plus the menu-replace note). Defaults I-1 to I-7 all accepted. Design is now ready to build; see `docs/INBOX_DESIGN.md`.

### Q11 · Docker is not reachable from WSL Ubuntu. Enable the integration?
**Answer (2026-10-03):** Done. `docker ps` in Ubuntu lists n8n, Jellyfin, cloudflared and nginx, and the LearnHouse DB and Redis containers came up.

### Q1 · Where does personal knowledge live: inside LearnHouse courses, or in new models?
**Answer (2026-10-03):** New models. Recorded as D-007.

### Q2 · Gemini or Ollama for embeddings?
**Answer (2026-10-03):** Ollama on DavidLab from the first run. Recorded as D-006 (accepted).

### Q5 · Source of truth once the app exists: `notes/` markdown or the database?
**Answer (2026-10-03):** App database, after a one-way import. Recorded as D-008.

### Q9 · Which Claude plan are you on?
**Answer (2026-10-03):** Pro. Fable runs only on usage credits, so Fable work is exactly what spends the $100 credit; Opus/Sonnet/Haiku use the plan limits.

