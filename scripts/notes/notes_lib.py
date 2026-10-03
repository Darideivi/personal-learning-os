"""Parser for the `notes/` knowledge base (stdlib only).

This is the reference for the future importer (docs/INBOX_DESIGN.md section 7):
the same rules, kept simple enough to port into the LearnHouse fork.
"""
import re
from pathlib import Path
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s]*[^\s.,;:)]", re.IGNORECASE)
INBOX_LINE_RE = re.compile(r"^- \[( |x|X)\] (.+)$")

TOPIC_STATUS = {"not-started", "learning", "practicing", "comfortable", "confident"}
RESOURCE_STATUS = {"to-do", "in-progress", "done"}
RESOURCE_KIND = {"youtube", "course", "article", "docs", "github", "pdf", "book", "lab", "tool"}
PROJECT_STATUS = {"idea", "active", "paused", "done"}
DOMAINS = {"ai", "python", "js-ts", "backend", "frontend", "devops", "security", "homelab"}


def parse_frontmatter(text):
    """Return (dict, body). Handles `key: value`, `[a, b]` lists, quotes and `# comments`."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, text
    data = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = re.sub(r"\s+#.*$", "", value).strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key.strip()] = [v.strip().strip("\"'") for v in inner.split(",")] if inner else []
        else:
            data[key.strip()] = value.strip("\"'")
    return data, "\n".join(lines[end + 1:])


def detect_type(text):
    """Mirror of the Inbox `detect_type` rules (first match wins). Returns (type, url)."""
    m = URL_RE.search(text)
    if not m:
        return "note", None
    url = m.group(0)
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if host in ("youtube.com", "m.youtube.com", "youtu.be"):
        return "youtube", url
    if host == "github.com":
        return "github", url
    if parsed.path.lower().endswith(".pdf"):
        return "pdf", url
    return "article", url


def parse_inbox_line(line):
    """Parse one `- [ ] ...` line into the InboxItem fields of the design (section 7)."""
    m = INBOX_LINE_RE.match(line.strip())
    if not m:
        return None
    status = "open" if m.group(1) == " " else "reviewed"
    text = m.group(2).strip()
    typ, url = detect_type(text)
    if url:
        rest = text.replace(URL_RE.search(text).group(0), "", 1).strip()
        if rest.startswith(":") or not rest:
            title, note = url, rest.lstrip(":").strip()
        else:
            title, _, note = rest.partition(":")
            title, note = title.strip(), note.strip()
    else:
        title, _, note = text.partition(":")
        title, note = title.strip(), note.strip()
    return {"status": status, "type": typ, "url": url, "title": title, "note": note,
            "source": "notes-import"}


def parse_inbox(path):
    return [i for i in (parse_inbox_line(l) for l in Path(path).read_text().splitlines()) if i]


def load_notes(root):
    """Yield (path, frontmatter, body) for every markdown file with frontmatter, skipping templates."""
    for p in sorted(Path(root).rglob("*.md")):
        if p.name.startswith("_") or p.name in ("README.md", "inbox.md"):
            continue
        fm, body = parse_frontmatter(p.read_text())
        yield p, fm, body


def check(root):
    """Return a list of (level, path, message). Levels: error, warn."""
    root = Path(root)
    out = []
    notes = list(load_notes(root))
    topic_ids = {p.stem for p, fm, _ in notes if fm.get("type") == "topic"}
    for p, fm, body in notes:
        rel = p.relative_to(root)
        typ = fm.get("type")
        if not typ:
            if p.name != "plan.md":
                out.append(("error", rel, "missing frontmatter `type`"))
            continue
        if not fm.get("title") and typ in ("topic", "resource", "project"):
            out.append(("error", rel, "missing `title`"))
        enum = {"topic": ("status", TOPIC_STATUS), "resource": ("status", RESOURCE_STATUS),
                "project": ("status", PROJECT_STATUS)}.get(typ)
        if enum and fm.get(enum[0]) not in enum[1]:
            out.append(("error", rel, f"`{enum[0]}` = {fm.get(enum[0])!r}, expected one of {sorted(enum[1])}"))
        if typ == "topic" and fm.get("domain") not in DOMAINS:
            out.append(("error", rel, f"`domain` = {fm.get('domain')!r}, expected one of {sorted(DOMAINS)}"))
        if typ == "resource" and fm.get("kind") not in RESOURCE_KIND:
            out.append(("error", rel, f"`kind` = {fm.get('kind')!r}"))
        for key in ("related", "topics"):
            for t in fm.get(key, []) or []:
                if t not in topic_ids:
                    out.append(("warn", rel, f"`{key}` references topic '{t}' with no file in notes/topics/"))
        for target in re.findall(r"\]\(([^)#]+\.md)\)", body):
            if not (p.parent / target).resolve().exists():
                out.append(("error", rel, f"broken link: {target}"))
    return out
