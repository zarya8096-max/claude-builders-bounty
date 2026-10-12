#!/usr/bin/env python3
"""
Test suite for Claude Code PR Reviewer CLI & Agent.
"""

import unittest
from claude_review import parse_pr_url, analyze_diff, format_review_markdown

class TestPRReviewer(unittest.TestCase):
    def test_parse_pr_url(self):
        owner, repo, pr_num = parse_pr_url("https://github.com/facebook/react/pull/12345")
        self.assertEqual(owner, "facebook")
        self.assertEqual(repo, "react")
        self.assertEqual(pr_num, 12345)

    def test_parse_pr_url_invalid(self):
        with self.assertRaises(ValueError):
            parse_pr_url("https://gitlab.com/owner/repo/pull/123")

    def test_analyze_diff_risk_detection(self):
        sample_diff = """diff --git a/script.sh b/script.sh
index 123..456 100644
--- a/script.sh
+++ b/script.sh
@@ -1,3 +1,4 @@
+rm -rf /data/cache
"""
        res = analyze_diff(sample_diff, "test", "repo", 1)
        self.assertTrue(any("destructive" in r.lower() for r in res["risks"]))

    def test_format_review_markdown(self):
        data = {
            "summary": "Sample summary text.",
            "risks": ["Risk 1"],
            "suggestions": ["Suggestion 1"],
            "confidence": "High",
            "files_count": 1
        }
        md = format_review_markdown(data, "https://github.com/test/repo/pull/1")
        self.assertIn("## 🤖 Claude Code PR Review", md)
        self.assertIn("Sample summary text.", md)
        self.assertIn("Risk 1", md)
        self.assertIn("Suggestion 1", md)
        self.assertIn("**High**", md)

if __name__ == "__main__":
    unittest.main()
