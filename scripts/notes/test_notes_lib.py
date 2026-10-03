import tempfile
import unittest
from pathlib import Path

import notes_lib as n


class DetectType(unittest.TestCase):
    def test_table(self):
        for text, want in [
            ("just an idea", "note"),
            ("https://youtu.be/abc", "youtube"),
            ("https://WWW.YouTube.com/watch?v=1", "youtube"),
            ("https://github.com/a/b: repo", "github"),
            ("https://x.org/paper.PDF", "pdf"),
            ("https://example.com/post", "article"),
        ]:
            self.assertEqual(n.detect_type(text)[0], want, text)


class InboxLine(unittest.TestCase):
    def test_url_with_description(self):
        i = n.parse_inbox_line("- [ ] https://github.com/nvidia/skillspector: security scanner")
        self.assertEqual((i["type"], i["status"], i["note"]), ("github", "open", "security scanner"))
        self.assertEqual(i["title"], "https://github.com/nvidia/skillspector")

    def test_name_with_repo_and_note(self):
        i = n.parse_inbox_line("- [x] claude-mem (thedotmack/claude-mem): memory across sessions")
        self.assertEqual((i["type"], i["status"], i["url"]), ("note", "reviewed", None))
        self.assertEqual((i["title"], i["note"]), ("claude-mem (thedotmack/claude-mem)", "memory across sessions"))

    def test_not_an_item(self):
        self.assertIsNone(n.parse_inbox_line("# Inbox"))


class Frontmatter(unittest.TestCase):
    def test_parse(self):
        fm, body = n.parse_frontmatter('---\ntype: topic\nrelated: [a, b]  # c\nreviewed:\ntitle: "X: Y"\n---\nbody')
        self.assertEqual(fm, {"type": "topic", "related": ["a", "b"], "reviewed": "", "title": "X: Y"})
        self.assertEqual(body, "body")

    def test_check_flags_problems(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d) / "topics"
            t.mkdir()
            (t / "a.md").write_text("---\ntype: topic\ntitle: A\nstatus: bad\ndomain: ai\nrelated: [ghost]\n---\n[x](missing.md)")
            msgs = [m for _, _, m in n.check(d)]
            self.assertTrue(any("status" in m for m in msgs))
            self.assertTrue(any("ghost" in m for m in msgs))
            self.assertTrue(any("broken link" in m for m in msgs))


if __name__ == "__main__":
    unittest.main()
