#!/usr/bin/env python3
"""Load notes/inbox.md into the LearnHouse Inbox through its HTTP API (stdlib only).

One-way (D-008): markdown is never written back. Dry-run is the default.

    python3 scripts/notes/import_inbox.py                  # print what would be imported
    LEARNHOUSE_API_URL=http://localhost:1338/api/v1 LEARNHOUSE_TOKEN=<jwt> \
    LEARNHOUSE_ORG_ID=1 python3 scripts/notes/import_inbox.py --apply

The token is read from the environment only; never put it in a file.
Idempotent: an item is skipped when one with the same url (or same title when
there is no url) already exists for the user, in any status.
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

LINE_RE = re.compile(r"^- \[( |x|X)\]\s+(.*\S)\s*$")
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


def parse_line(line: str):
    """Return {text, note, reviewed} for a checklist line, or None for other lines.

    `text` goes to the API's one capture field (it detects type/url/title itself);
    `note` is the description after the first ':'.
    """
    m = LINE_RE.match(line)
    if not m:
        return None
    reviewed = m.group(1) in "xX"
    body = m.group(2)
    u = URL_RE.search(body)
    if u:
        url = u.group(0).rstrip(":,.;)")
        before = body[: u.start()].strip()
        rest = body[u.start() + len(url):].lstrip(":,. ").strip()
        text = f"{before} {url}".strip()
        note = rest
    else:
        head, sep, tail = body.partition(": ")
        text, note = (head.strip(), tail.strip()) if sep else (body, "")
    return {"text": text, "note": note, "reviewed": reviewed}


def parse_inbox(markdown: str):
    return [item for item in map(parse_line, markdown.splitlines()) if item]


def _key(text: str) -> str:
    u = URL_RE.search(text)
    return (u.group(0) if u else text).strip().lower()


def _request(method, url, token, body=None):
    req = urllib.request.Request(
        url,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as res:
        return json.load(res)


def apply(items, api, token, org_id):
    existing = _request("GET", f"{api}/inbox/org/{org_id}?status=all&limit=200", token)
    seen = {_key(e["url"] or e["title"]) for e in existing}
    created = skipped = 0
    for item in items:
        if _key(item["text"]) in seen:
            skipped += 1
            continue
        made = _request("POST", f"{api}/inbox/", token,
                        {"org_id": org_id, "text": item["text"], "note": item["note"]})
        if item["reviewed"]:
            _request("PATCH", f"{api}/inbox/{made['inbox_item_uuid']}", token,
                     {"status": "reviewed"})
        seen.add(_key(item["text"]))
        created += 1
    return created, skipped


def main(argv):
    path = Path(__file__).resolve().parents[2] / "notes" / "inbox.md"
    items = parse_inbox(path.read_text(encoding="utf-8"))
    if "--apply" not in argv:
        for i in items:
            print(json.dumps(i, ensure_ascii=False))
        print(f"{len(items)} item(s) parsed (dry run, nothing sent)")
        return 0
    api = os.environ["LEARNHOUSE_API_URL"].rstrip("/")
    token = os.environ["LEARNHOUSE_TOKEN"]
    org_id = int(os.environ["LEARNHOUSE_ORG_ID"])
    created, skipped = apply(items, api, token, org_id)
    print(f"created {created}, skipped {skipped} already present")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
