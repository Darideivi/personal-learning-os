import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_notes
import import_inbox


class ParseInbox(unittest.TestCase):
    def test_url_with_description(self):
        r = import_inbox.parse_line("- [ ] https://github.com/nvidia/skillspector: security scanner, check first")
        self.assertEqual(r, {"text": "https://github.com/nvidia/skillspector",
                             "note": "security scanner, check first", "reviewed": False})

    def test_url_with_moved_to_parenthetical_stays_in_note(self):
        r = import_inbox.parse_line("- [ ] https://github.com/public-apis/public-apis: huge list (moved to resources/public-apis.md)")
        self.assertEqual(r["text"], "https://github.com/public-apis/public-apis")
        self.assertTrue(r["note"].endswith("(moved to resources/public-apis.md)"))

    def test_name_without_url(self):
        r = import_inbox.parse_line("- [ ] claude-mem (thedotmack/claude-mem): memory across sessions")
        self.assertEqual(r["text"], "claude-mem (thedotmack/claude-mem)")
        self.assertEqual(r["note"], "memory across sessions")

    def test_checked_is_reviewed_and_plain_line(self):
        self.assertTrue(import_inbox.parse_line("- [x] an idea")["reviewed"])
        self.assertEqual(import_inbox.parse_line("- [ ] an idea")["note"], "")

    def test_non_items_ignored(self):
        self.assertIsNone(import_inbox.parse_line("# Inbox"))
        self.assertIsNone(import_inbox.parse_line("Capture fast."))

    def test_real_inbox_file(self):
        text = (Path(__file__).resolve().parents[2] / "notes" / "inbox.md").read_text(encoding="utf-8")
        items = import_inbox.parse_inbox(text)
        self.assertEqual(len(items), 5)
        self.assertTrue(all(i["text"] and not i["text"].endswith(":") for i in items))


class CheckNotes(unittest.TestCase):
    def test_frontmatter(self):
        fm = check_notes.parse_frontmatter("---\ntype: topic\nstatus: learning   # x\n---\n# T\n")
        self.assertEqual(fm, {"type": "topic", "status": "learning"})
        self.assertIsNone(check_notes.parse_frontmatter("# no block"))

    def test_real_notes_pass(self):
        self.assertEqual(check_notes.main(["x"]), 0)


if __name__ == "__main__":
    unittest.main()
