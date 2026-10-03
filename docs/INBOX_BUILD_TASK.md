# Inbox build task (cloud session, items 1 to 7)

The spec is `docs/INBOX_DESIGN.md` (APPROVED 2026-10-03, with four amendments). This file is the task brief for a cloud Claude Code session. Code goes in the fork `Darideivi/learnhouse` on a new branch `feat/learning-inbox`, created from upstream `dev`. Docs updates go in `personal-learning-os`.

## Read first, in order

`CLAUDE.md`, `docs/STATUS.md`, `docs/OPEN_QUESTIONS.md`, `docs/INBOX_DESIGN.md`, `docs/ARCHITECTURE_NOTES.md` sections 4, 8 and 10.

## Deliverables (match INBOX_DESIGN sections 2 to 8)

1. `apps/api/src/db/inbox/inbox_items.py`: `InboxItem` model, `InboxItemType` and `InboxItemStatus` enums, Create/Update/Read schemas, composite index, `inbox_` uuid, str dates, `source` and `reviewed_date`.
2. `apps/api/src/services/inbox/inbox.py`: create, list (status filter, paging, newest first), get, patch (sets or clears `reviewed_date`), delete, and `detect_type()`.
   - Every query filters on the caller's `user_id` (other users' items return 404).
   - Gate org access with `require_org_membership(resolve_acting_user_id(...))`.
   - Validation (section 4 amendment): only http/https URLs on create AND on PATCH; empty or whitespace-only text returns 422; length limits (text and title 500, note 10,000, url 2,048).
3. `apps/api/src/routers/inbox/inbox.py` with the five routes in section 4, mounted with prefix `/inbox` and `require_authenticated_user` in `src/router.py`. That `router.py` change must be the ONLY edit to an existing upstream file.
4. API tests: `src/tests/routers/test_inbox_router.py` (cases 1 to 9 in section 8, including the unpatched `other_org` 403 test and the validation cases) and `src/tests/services/test_inbox_detect_type.py` (parametrized, incl. `youtu.be`, uppercase hosts, `.PDF`). Follow the app and fixture pattern in `src/tests/routers/test_folders_router.py`.
5. Web: `apps/web/services/inbox/inbox.ts`, and under `app/orgs/[orgslug]/(withmenu)/inbox/`: `page.tsx`, `InboxClient.tsx`, `inbox-list.tsx`. Follow the Library page patterns named in section 6. Quick-capture input, Open/Reviewed/All tabs, Reviewed action, Edit/Archive/Delete menu, render `url` as a link only when it starts with `http://` or `https://`. No upstream UI edits, no new dependencies.
6. `apps/e2e/features/inbox/tests/capture.spec.ts`: the single capture, list, mark-reviewed flow from section 8. Use `E2E_BASE_URL` (that skips the boot). Never put a real password in any file.
7. `apps/api/migrations/versions/<new_rev>_add_inbox_item.py`, written by hand because there is no database in the cloud. Find the current Alembic head by following the `down_revision` chain in the version files (not the newest filename). Create the `inboxitem` table, its indexes and both enum types (`inboxitemtype`, `inboxitemstatus`). The downgrade drops the table and both types. Mirror how an existing upstream migration creates tables and enums.

## Rules

- The cloud sandbox cannot run Docker, Postgres or the LearnHouse stack, and cannot download Python 3.14.7. Do not try. If the image happens to have a compatible Python, you may run only pure unit tests such as `test_inbox_detect_type.py`. Everything else is verified later on DavidLab. Never claim code is tested unless you actually ran it.
- Follow section 5 for file layout and reuse the patterns it names. Keep it minimal: no webhooks, analytics, AI or RBAC changes. Do not edit `check_element_type`, query keys, menu components or i18n files.
- No real keys or passwords in any file. No force-push. Push only the branch `feat/learning-inbox` to `Darideivi/learnhouse` (never to upstream, `dev` or `main`). Do not open a pull request.
- Small logical commits, one per deliverable above, with clear messages.
- Anything that needs David goes into `docs/OPEN_QUESTIONS.md` with a default. If the design and the real source disagree, follow the real source, note it in `docs/LEARNING_LOG.md`, and continue.

## When finished

Update `docs/STATUS.md` in `personal-learning-os` with what was built per deliverable, the branch name and last commit, and this verification checklist for DavidLab, in order:

a. Stop the API process first (INBOX_DESIGN section 3, hot-reload trap), pull the branch, run `uv run alembic upgrade head`, confirm the `inboxitem` table and both enum types exist, then run the downgrade and upgrade once more.
b. Run only `cd apps/api && uv run pytest src/tests/routers/test_inbox_router.py src/tests/services/test_inbox_detect_type.py -q 2>&1 | tee /tmp/inbox-tests.log`.
c. Restart the API and web, then capture a YouTube URL in the browser at `/orgs/default/inbox` and mark it reviewed.
d. Add the Inbox menu link by resending the whole menu list with the custom item (INBOX_DESIGN section 6 amendment).
e. Run the Playwright spec with `E2E_BASE_URL=http://localhost:3000` plus the admin email and password env vars.
f. Run the full API suite once in the background with output to a log file.
