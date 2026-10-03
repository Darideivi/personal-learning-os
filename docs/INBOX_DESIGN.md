# Personal Learning Inbox: Design

**Status: Draft. Q1 and Q5 confirmed by David on 2026-10-03 (D-007: new model, not a course; D-008: one-way import, database is the source of truth). Needs David's approval (OPEN_QUESTIONS Q10) before `/ecc:feature-dev`.**

| | |
|---|---|
| Upstream base | `learnhouse/learnhouse`, branch `dev`, commit `5e28b07` |
| Written | 2026-10-03, cloud session (source read, not run) |
| Branch | `feat/learning-inbox` in `Darideivi/learnhouse` |
| Related | `CLAUDE.md` (Core Product Areas), `ARCHITECTURE_NOTES.md` §4, §8, §10, `start.md` Prompt 2 |

## 1. Goal and scope

The Inbox is the **Capture** step of the loop. Paste a link or a line of text, it is saved in under a second, and it waits in a list until Sunday's review. Nothing else.

**v1 does**

- One text field: paste a URL or type a note, press Enter, item appears at the top of the list.
- Cheap deterministic type detection from the URL host (YouTube, GitHub, PDF, else article; no URL means note).
- List of items, open first, with a filter for `open` / `reviewed` / `all`.
- Mark an item reviewed (and back to open). Edit title/note/type inline. Delete.
- Scoped to the signed-in user inside the org. Only members of the org can see the org's items.

**v1 does not**

- No fetching of page titles, thumbnails, transcripts or metadata (no outbound HTTP, no background jobs).
- No AI (summaries, tags, concept extraction). Phase 2.
- No "promote to Resource / Topic". Those models don't exist yet. The `status` ladder leaves room for it (§2).
- No importer. The `notes/inbox.md` seeding is a later session; §7 only fixes the mapping so the model can hold it.
- No Library/Folder integration, no search integration, no RAG. The `inbox_` UUID prefix keeps the door open.

## 2. Data model

New table `inboxitem`, file `apps/api/src/db/inbox/inbox_items.py`. Pattern: `src/db/folders/folders.py` (Base / table / Create / Update / Read split, `org_id` FK with `ondelete="CASCADE"`, prefixed UUID string column) and `src/db/trails.py` (`user_id` FK + composite `Index("ix_trail_user_org", ...)`). Enums follow `src/db/courses/activities.py` (`class ActivityTypeEnum(str, Enum)`).

```python
class InboxItemType(str, Enum):
    YOUTUBE = "youtube"; ARTICLE = "article"; GITHUB = "github"; PDF = "pdf"
    COURSE = "course"; DOCS = "docs"; IDEA = "idea"; LAB = "lab"
    PROJECT = "project"; NOTE = "note"; COMMAND = "command"

class InboxItemStatus(str, Enum):
    OPEN = "open"            # just captured
    REVIEWED = "reviewed"    # looked at on Sunday, kept for later
    ARCHIVED = "archived"    # done with it (promoted elsewhere or dropped)

class InboxItemBase(SQLModel):
    type: InboxItemType = InboxItemType.NOTE
    url: Optional[str] = None            # None for ideas/notes/commands
    title: str                           # required; defaults to the URL or first 80 chars of text
    note: Optional[str] = ""             # my words, free text
    status: InboxItemStatus = InboxItemStatus.OPEN

class InboxItem(InboxItemBase, table=True):
    __table_args__ = (Index("ix_inboxitem_user_org_status", "user_id", "org_id", "status"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    inbox_item_uuid: str = Field(default="", index=True)     # "inbox_<uuid4>"
    org_id: int   # FK organization.id, ondelete CASCADE, index
    user_id: int  # FK user.id, ondelete CASCADE, index
    source: Optional[str] = None         # "web" | "notes-import"; set by the importer (§7)
    creation_date: str = ""              # upstream convention: str(datetime.now()), not datetime
    update_date: str = ""
    reviewed_date: Optional[str] = None  # set when status leaves "open"

class InboxItemCreate(SQLModel):
    org_id: int
    text: str                            # the one field from the UI; server splits url/title/type
    type: Optional[InboxItemType] = None # override auto-detection
    note: Optional[str] = ""

class InboxItemUpdate(SQLModel):         # all optional: title, note, type, status, url
class InboxItemRead(InboxItemBase):      # + id, inbox_item_uuid, org_id, user_id, source, dates
```

Choices:

- **`creation_date` as `str`** matches every upstream table (`Folder`, `Trail`), so the autogenerate diff is clean and Alembic needs no enum/datetime surprises. Phase 3 can migrate to `datetime` across our own tables at once.
- **Prefixed UUID `inbox_`** follows `FolderContent.resource_uuid` (`src/db/folders/folder_content.py` docstring). It is only a stable public id in v1; registering it in `src/security/rbac/utils.py::check_element_type` is deliberately **not** done (that is an upstream edit, see §5).
- **`source` and `reviewed_date`** are the only fields beyond the Prompt 2 list. `source` keeps imported items distinguishable so the importer is re-runnable; `reviewed_date` is one column that answers "what did I process this week" without a log table. Drop either if David prefers the strict list.
- Enum columns: SQLModel maps `str, Enum` to a Postgres `ENUM` type; `migrations/env.py` imports `alembic_postgresql_enum`, so the migration gets the `CREATE TYPE` for free. Adding a value later is one `op.sync_enum_values` migration.

## 3. Migration plan

`ARCHITECTURE_NOTES.md` §8: a fresh dev DB comes from `SQLModel.metadata.create_all` at startup, and Alembic has never run there. `src/core/events/database.py::import_all_models()` and `migrations/env.py` both walk `src/db/` recursively, so the new file under `src/db/inbox/` is picked up by both without registration.

```bash
cd apps/api
uv run alembic current                 # expect: no revision
uv run alembic stamp head              # ONCE, on the existing dev DB, before adding the model
# add src/db/inbox/inbox_items.py
uv run alembic revision --autogenerate -m "add inbox_item"
# review: one create_table + indexes + CREATE TYPE for the two enums, nothing else
uv run alembic upgrade head
```

Fresh-DB check (required because `create_all` hides a missing migration): drop the `learnhouse-db-dev` volume, start with the model present, run `alembic stamp head` minus one revision, then `upgrade head`, and confirm `inboxitem` exists. Record the exact step order in `LEARNING_LOG.md`. Downgrade must drop the table and both enum types.

## 4. API

Mount: `v1_router.include_router(inbox.router, prefix="/inbox", tags=["inbox"], dependencies=[Depends(require_authenticated_user)])` in `src/router.py`, the same line shape as the `trail` router (session user only, API tokens and anonymous rejected at the router level). Router file follows `src/routers/trail.py` (thin handlers, `Depends(get_current_user)` + `Depends(get_db_session)`, `summary` / `description` / `responses` on each route); service follows `src/services/folders/folders.py` for the org check and UUID/date conventions.

| Method | Path | Body / query | Returns | Notes |
|---|---|---|---|---|
| `POST` | `/inbox/` | `InboxItemCreate` | `InboxItemRead` | Detects type from URL (§6), fills `title`, sets `user_id` from the session |
| `GET` | `/inbox/org/{org_id}` | `?status=open\|reviewed\|archived\|all` (default `open`), `?page=1&limit=50` | `List[InboxItemRead]` | Only the caller's items, newest first |
| `GET` | `/inbox/{inbox_item_uuid}` | | `InboxItemRead` | 404 if not found or not the caller's |
| `PATCH` | `/inbox/{inbox_item_uuid}` | `InboxItemUpdate` | `InboxItemRead` | Status change sets/clears `reviewed_date` |
| `DELETE` | `/inbox/{inbox_item_uuid}` | | `{"detail": "deleted"}` | Hard delete; it's an inbox |

Auth and permission checks, copied from `src/services/folders/folders.py::create_folder`:

1. Router-level `require_authenticated_user` (`src/router.py`) rejects anonymous and API-token users.
2. In the service, `await require_org_membership(resolve_acting_user_id(current_user), org_id, db_session)` (`src/security/org_auth.py`, `src/security/auth.py`). The org id comes from the body or path, exactly the case the folders docstring warns about, so it is gated explicitly.
3. Ownership: every query adds `InboxItem.user_id == user_id`. Items of another user in the same org return 404, not 403 (don't reveal existence). No `check_resource_access` call: `inbox_` is unknown to `check_element_type`, and the item is private to one user, so role-based RBAC adds nothing in v1. Written down so the security review knows it was a choice.

Not in v1: webhooks (`dispatch_webhooks`), analytics, `ResourceAuthor` rows.

## 5. File layout and upstream edits

All new code lives in an `inbox` folder per layer, mirroring how upstream groups `folders/`.

```text
apps/api/src/db/inbox/__init__.py
apps/api/src/db/inbox/inbox_items.py           model + enums + schemas        (pattern: db/folders/folders.py)
apps/api/src/services/inbox/__init__.py
apps/api/src/services/inbox/inbox.py           CRUD + detect_type()           (pattern: services/folders/folders.py)
apps/api/src/routers/inbox/__init__.py
apps/api/src/routers/inbox/inbox.py            FastAPI router                 (pattern: routers/trail.py)
apps/api/migrations/versions/<rev>_add_inbox_item.py
apps/api/src/tests/routers/test_inbox_router.py                               (pattern: tests/routers/test_folders_router.py)
apps/api/src/tests/services/test_inbox_detect_type.py

apps/web/services/inbox/inbox.ts               fetch helpers                  (pattern: services/folders/folders.ts)
apps/web/app/orgs/[orgslug]/(withmenu)/inbox/page.tsx        server page      (pattern: (withmenu)/library/page.tsx, minus SEO)
apps/web/app/orgs/[orgslug]/(withmenu)/inbox/InboxClient.tsx 'use client'     (pattern: library/LibraryClient.tsx)
apps/web/app/orgs/[orgslug]/(withmenu)/inbox/inbox-list.tsx  row + inline edit (pattern: library/library-cards.tsx)

apps/e2e/features/inbox/tests/capture.spec.ts  one Playwright flow            (pattern: features/assignments/tests/*.spec.ts)
```

**Edits to existing upstream files: exactly one.** `apps/api/src/router.py`: one import line and one `include_router` block. Everything else is additive, so an upstream merge conflicts at most on that one hunk.

Deliberately avoided: `src/security/rbac/utils.py::check_element_type` (not needed without RBAC), `lib/query/keys.ts` (the client defines its own `['inbox', orgId, status]` key inline), `OrgMenuLinks.tsx` (see §6), i18n files (labels hard-coded in English in our own components; single user).

## 6. Web

**Route** `/orgs/{orgslug}/inbox`, under `(withmenu)` so it gets the org menu and session context like Library. `page.tsx` only resolves `orgslug` and renders the client component (the Library page's `generateMetadata` block is skipped; this page is private).

**InboxClient.tsx**, following `LibraryClient.tsx`: `useOrg()` for `org.id`, `useLHSession()` for the access token, `useQuery` from `@tanstack/react-query` for the list, `useMutation` + `invalidateQueries` for create/patch/delete. Layout inside `GeneralWrapperStyled`, title via `TypeOfContentTitle`, so it matches upstream pages.

**Quick capture**: one `<input>` at the top, autofocus, placeholder "Paste a link or type a thought, press Enter". Enter posts `{org_id, text}`. The input clears on success and the item appears at the top (optimistic update is a nice-to-have, not v1). Nothing else is asked at capture time: save now, organize later.

**Type detection** lives server-side in `services/inbox/inbox.py::detect_type(text)` so the importer and the API agree, with the same table mirrored client-side only to show the icon before the response:

| Rule (first match wins) | Type |
|---|---|
| no `http(s)://` token in the text | `note` |
| host `youtube.com`, `youtu.be` | `youtube` |
| host `github.com` | `github` |
| path ends with `.pdf` | `pdf` |
| any other URL | `article` |

`title` = text with the URL removed and trimmed, or the URL itself when nothing is left. `url` = the first URL token. Trailing "(moved to …)" style parentheticals are kept in `note` as written. Anything smarter (page titles, oEmbed) is Phase 2.

**List**: rows, not cards. Each row: type icon (phosphor), title (link when `url` is set, `target="_blank"`), note in muted text, relative date, and two actions: **Reviewed** (PATCH `status=reviewed`) and a kebab with Edit / Archive / Delete. Filter tabs `Open · Reviewed · All`. Empty state: one line.

**Nav entry, zero upstream UI edits**: `OrgMenuLinks.tsx` already renders `type: "custom"` items from `OrganizationConfig.menu.items` (`MenuLinkItem` in `src/db/organization_config.py`), and a relative `url` goes through `getUriWithOrg(orgslug, url)`, so `{type: "custom", label: "Inbox", url: "/inbox", icon: "Lightbulb", order: 0}` puts Inbox in the top menu. It is set from Dashboard → Organization → Menu (`components/Dashboard/Pages/Org/OrgEditMenu/OrgEditMenu.tsx`) and recorded in `DECISIONS.md` under "Org settings to apply". `Lightbulb` is the closest icon in the curated `MENU_ICONS` set (`components/Objects/Menus/menuIcons.tsx`); there is no tray icon. Phase 1's larger nav (Dashboard · Learn · Knowledge …) is when a real menu edit is justified, not now.

## 7. Seeding from `notes/inbox.md`

Importer is a later session (start.md Prompt 3). The model must already fit the file, whose shape is one `- [ ] <text>` line per item, where text is `URL: description` or `name (owner/repo): description`:

| Markdown | InboxItem |
|---|---|
| `- [ ]` | `status=open`; `- [x]` → `reviewed` |
| first URL token | `url`; `detect_type()` gives `type` (github / article / …) |
| text before the first `:` after the URL, or the whole line without URL | `title` (e.g. `claude-mem (thedotmack/claude-mem)`) |
| text after that `:` | `note` (e.g. `security scanner for AI agent skills, check before installing skills`) |
| `(moved to resources/public-apis.md)` | stays inside `note` in v1; a later pass turns it into a Resource link |
| everything | `source="notes-import"`, `user_id` = admin, `org_id` = the single org |

Idempotency: skip a line when an item with the same `url` (or same `title` when no URL) and `source="notes-import"` already exists. One-way (Q5 default): the importer never writes back to markdown. The `topics/`, `resources/`, `projects/` frontmatter files are **not** Inbox items; they wait for the `Resource` and `Topic` models.

## 8. Tests

**API** (`src/tests/routers/test_inbox_router.py`, in-memory SQLite via `conftest.py`; app fixture copied from `test_folders_router.py`: `FastAPI()` + `include_router(router, prefix="/api/v1/inbox")` + `dependency_overrides` for `get_db_session` and `get_current_user`; patch `src.services.inbox.inbox.require_org_membership` the way folders tests patch `check_resource_access`, plus one test that leaves it unpatched with the `other_org` fixture and expects 403):

1. create from a YouTube URL → `type=youtube`, `url` set, `title` is the remaining text, uuid starts with `inbox_`.
2. create from plain text → `type=note`, `url is None`, `title` is the text.
3. create with explicit `type=command` overrides detection.
4. list defaults to `status=open`, newest first; `?status=all` includes reviewed.
5. items of `regular_user` are invisible to `admin_user` (list excludes, GET/PATCH/DELETE return 404).
6. PATCH to `reviewed` sets `reviewed_date`; PATCH back to `open` clears it.
7. delete then GET → 404.
8. `other_org` → 403 on create and list.

`src/tests/services/test_inbox_detect_type.py`: a parametrized table for the §6 rules, including `youtu.be`, uppercase hosts and a `.PDF` suffix.

**Playwright** (`apps/e2e/features/inbox/tests/capture.spec.ts`, `test` from `core/fixtures.ts`, `storageState` = the admin session, pointed at the dev stack with `E2E_BASE_URL=http://localhost:3000` so no self-host boot): log in → open `/inbox` → paste a YouTube URL + a word → Enter → row appears with the YouTube icon → click **Reviewed** → row leaves the Open tab and appears under Reviewed. That is the whole "capture → list → mark reviewed" flow from Prompt 2. ⏳ confirm during the build that `E2E_SKIP_BOOT` works against `npx learnhouse dev` (ARCHITECTURE_NOTES §8 open item).

## 9. Open decisions for David

Guesses beyond the Q1/Q5 defaults. Each has a default so the build can start.

| # | Question | Default taken |
|---|---|---|
| I-1 | Three statuses (`open / reviewed / archived`) or just two (`open / reviewed`)? Prompt 2 says "mark as reviewed". | Three. `archived` is cheap and keeps the list clean once items are promoted. |
| I-2 | Keep `source` and `reviewed_date`, or strictly the Prompt 2 field list? | Keep both (one column each, both serve the importer and the weekly review). |
| I-3 | `creation_date` as upstream-style `str`, or a proper `datetime` for our own tables from day one? | `str`, for consistency with upstream and a clean autogenerate. Revisit in Phase 3. |
| I-4 | Hard delete, or soft delete via `archived` only? | Hard delete available; the UI puts Archive first. |
| I-5 | Nav via a `custom` menu link (DB setting, `Lightbulb` icon) vs editing `OrgMenuLinks.tsx` for a proper icon and i18n label? | Custom link, zero code. |
| I-6 | Per-user scoping even though there is one user? | Yes; `user_id` costs nothing now and Phase 6 would need it anyway. |
| I-7 | Should the Playwright spec live in upstream `apps/e2e` (needs the harness's `E2E_SKIP_BOOT` path) or as a small standalone Playwright CLI check in this repo? | `apps/e2e`, following the module layout its README describes. |
