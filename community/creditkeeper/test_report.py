import subprocess
import sys
import unittest
from pathlib import Path

from report import render_report


def row(kind, ref, amount, original="", vendor="sample supplier"):
    return dict(type=kind, vendor=vendor, reference=ref, amount=amount,
                original_invoice=original, note="PRIVATE NOTE MUST NOT APPEAR")


class ReportTests(unittest.TestCase):
    def test_missing_credit_and_notes(self):
        html = render_report([row("invoice", "inv", "200"),
                              row("expected_credit", "return", "75", "inv"),
                              row("posted_credit", "credit", "25", "inv")])
        self.assertIn("Suspected missing credit", html)
        self.assertIn("<td>50.00</td>", html)
        self.assertIn("return, credit", html)
        self.assertNotIn("PRIVATE NOTE MUST NOT APPEAR", html)

    def test_untrusted_references_are_text(self):
        html = render_report([row("expected_credit", '<script>alert(1)</script>', "20", 'x<img src=x>')])
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("Needs invoice evidence", html)

    def test_excess_is_not_missing(self):
        html = render_report([row("invoice", "inv", "100"), row("posted_credit", "credit", "20", "inv")])
        self.assertIn("Suspected excess credit", html)
        self.assertNotIn("Suspected missing credit", html)

    def test_balanced_orphan_still_needs_evidence(self):
        html = render_report([row("expected_credit", "return", "20", "inv"), row("posted_credit", "credit", "20", "inv")])
        self.assertIn("Needs invoice evidence", html)
        self.assertIn("<td>0.00</td>", html)

    def test_empty_does_not_claim_recovery(self):
        self.assertIn("does not establish", render_report([]))

    def test_invalid_input_fails_before_html(self):
        with self.assertRaises(ValueError):
            render_report([row("invoice", "inv", "1e3")])
        proc = subprocess.run([sys.executable, str(Path(__file__).with_name("report.py"))], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")


if __name__ == "__main__":
    unittest.main()
