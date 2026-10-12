# Destructive Command Blocker for Claude Code 🛡️

A lightweight, zero-dependency `pre-tool-use` hook for Claude Code that prevents accidental destruction of databases, git trees, and filesystems.

---

## ⚡ Quick Install (2 Commands)

```bash
mkdir -p ~/.claude/hooks && curl -sSL https://raw.githubusercontent.com/zarya8096-max/claude-builders-bounty/main/hooks/destructive-command-blocker/pre-tool-use.py -o ~/.claude/hooks/pre-tool-use.py
chmod +x ~/.claude/hooks/pre-tool-use.py && echo '{"hooks":{"preToolUse":"python3 ~/.claude/hooks/pre-tool-use.py"}}' >> ~/.claude/config.json
```

---

## 🔒 Protected Operations

The hook automatically intercepts and rejects the following dangerous patterns:

| Pattern | Description | Allowed Variant |
|---|---|---|
| `rm -rf <path>` | Recursive force deletion of directories | `rm <file>` (non-recursive) |
| `DROP TABLE <table>` | Dropping database tables | Table alterations, `CREATE TABLE` |
| `git push --force` / `-f` | Overwriting remote commit histories | `git push`, branch pushes |
| `TRUNCATE [TABLE]` | Purging table records without constraints | Standard selects, inserts |
| `DELETE FROM <table>` (no WHERE) | Unbounded deletion of entire tables | `DELETE FROM table WHERE id = ?` |

---

## 📝 Audit Logging

Every intercepted attempt is logged to `~/.claude/hooks/blocked.log`:

```log
[2026-10-12T10:02:57.664174] BLOCKED
  Command:      DELETE FROM users;
  Project Path: /workspace/my-app
  Reason:       Unbounded table deletion ('DELETE FROM' without WHERE clause) detected.
------------------------------------------------------------
```

---

## 🧪 Test Verification

Run the included automated test suite:

```bash
python3 test_hook.py
```

Result: `20 passed, 0 failed` across all edge cases (split flags, lowercase queries, safe queries).
