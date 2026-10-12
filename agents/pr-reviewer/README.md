# Claude Code PR Reviewer Agent 🤖

An automated Pull Request reviewer for Claude Code and GitHub Actions. Takes any PR diff, performs static and risk analysis, and outputs structured Markdown review comments with confidence scoring.

---

## ⚡ CLI Usage

```bash
python3 agents/pr-reviewer/claude_review.py --pr https://github.com/owner/repo/pull/123
```

Write directly to an output file:
```bash
python3 agents/pr-reviewer/claude_review.py --pr https://github.com/owner/repo/pull/123 --output review.md
```

---

## 🚀 GitHub Action Integration

Copy `.github/workflows/claude-pr-review.yml` into your repository. Whenever a Pull Request is opened or synchronized, the agent runs automatically and posts a structured comment.

---

## 📊 Structured Output Format

Every review includes:
1. **Summary of changes:** 2–3 sentences describing diff scope and file modifications.
2. **Identified risks:** Security hazards, destructive operations, or missing credentials.
3. **Improvement suggestions:** Architectural and test coverage recommendations.
4. **Confidence score:** `Low` / `Medium` / `High` based on test presence and complexity.

Real verification samples tested against repository PRs are available in `examples/`:
- `examples/review_pr4791.md` (Tested on PR #4791)
- `examples/review_pr4792.md` (Tested on PR #4792)

---

## 🧪 Testing

```bash
python3 test_pr_reviewer.py
```
