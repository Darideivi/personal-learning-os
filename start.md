# Start Here (Homelab)

## Before the first chat (about 15 min, by hand)

1. Install **Docker** (with Compose v2), **Node 18+**, **Git**, **gh** (GitHub CLI) and **Claude Code**. Run `gh auth login`.
2. Clone this repo and create your env file:
   ```bash
   git clone https://github.com/Darideivi/personal-learning-os.git
   cd personal-learning-os
   cp .env.example .env
   ```
3. Put your real keys in `.env` (Anthropic and OpenAI to start; the rest can wait).
4. Open Claude Code **inside `personal-learning-os/`** and paste Prompt 1.

The plan is three short sessions, not one giant one. That uses fewer tokens, and you understand each step before the next.

---

## Prompt 1: Get LearnHouse running and understood

```text
Read CLAUDE.md, start.md and notes/README.md first. Use ECC as the workflow.
I'm on my personal homelab machine (16 GB RAM, 500 GB SSD). This is where we build and run.

Goal: LearnHouse running locally, trimmed for one personal user, and documented. No custom features yet.

1. Check my machine: docker, docker compose, node, git, gh versions. Tell me if anything is missing and stop if it is.
2. Fork learnhouse/learnhouse to Darideivi/learnhouse and clone it NEXT TO this repo (../learnhouse), not inside it. Add the upstream remote.
3. Merge the values from this repo's .env into whatever `npx learnhouse dev` expects. Confirm the AI provider strings in apps/api/config/config.py and fix .env.example here if they're wrong.
4. Run `npx learnhouse dev` until web, API, collab, Postgres and Redis are healthy. Create a local admin. Give me the URL to open.
5. Hide what I don't need, using config and navigation only and never deleting upstream code. Follow the "Run it whole, hide what I don't need" table in CLAUDE.md.
6. Run `graphify .` in ../learnhouse, then use ecc:codebase-onboarding to write ../learnhouse/docs/ARCHITECTURE_NOTES.md: how web → API → database flows, where courses/activities/progress/auth/AI-RAG live, and how migrations and tests run.
7. Update "Important Commands" in CLAUDE.md with the real commands. Start docs/DECISIONS.md in ../learnhouse with what we hid and why.
8. Add what I learned (Docker, env vars, anything that broke) to notes/journal/ for this week.

Explain each step simply as you go: what it does and what concept I'm learning.
Stop when it runs and the notes are written. Don't start the Inbox.
```

---

## Prompt 2: Build the Learning Inbox (next session)

```text
Read CLAUDE.md and ../learnhouse/docs/ARCHITECTURE_NOTES.md. Use ECC.
Build the Personal Learning Inbox in ../learnhouse on branch feat/learning-inbox, following how LearnHouse already does things.

1. /ecc:plan first: show me the design (model, migration, API, page, nav entry) and wait for my OK.
2. Build it with ecc:tdd-guide: SQLModel InboxItem (type, url, title, note, status, created_at, user/org), Alembic migration, FastAPI CRUD router, Next.js /inbox page with one-field quick capture plus a list, mark as reviewed, and a nav entry.
3. Tests: API tests plus one Playwright check (capture → list → mark reviewed).
4. Review with ecc:python-reviewer, ecc:typescript-reviewer and ecc:security-reviewer. Fix what matters.
5. Log the decision in docs/DECISIONS.md. Explain the key files to me like a lesson.
Commit on the branch. Don't push or merge until I say so.
```

---

## Prompt 3: Import my notes (session after that)

```text
Read CLAUDE.md. Use ECC.
Write a small importer that reads notes/ (frontmatter: type, status, topics…) from the personal-learning-os repo
and loads notes/inbox.md items into the Inbox. Plan first, then build with tests.
Show me my Jeff Su video and AI topics inside the app when done.
```

---

## Side quest (any time)

Install **INDEX 0** from https://www.index-0.in on the homelab, explore it, and write what you liked in `notes/inbox.md`. Never install it on the work laptop.

## Every day, even without the app

Learned something? Add one line to `notes/inbox.md`. Then `git add -A && git commit -m "notes" && git push`.
