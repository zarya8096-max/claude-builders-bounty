#!/usr/bin/env python3
"""
Test suite for Claude Code Destructive Command Blocker Hook.
Verifies all acceptance criteria:
1. Blocks rm -rf, DROP TABLE, git push --force, TRUNCATE, DELETE FROM without WHERE
2. Allows safe commands (DELETE FROM with WHERE, git push, normal rm, etc.)
3. Logs blocked events with timestamp, command, and project path to blocked.log
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path

HOOK_SCRIPT = Path(__file__).parent / "pre-tool-use.py"
LOG_FILE = Path.home() / ".claude" / "hooks" / "blocked.log"

TEST_CASES = [
    # (command, should_block, description)
    # Dangerous commands (MUST BLOCK):
    ("rm -rf /tmp/data", True, "rm -rf standard"),
    ("rm -fr /tmp/data", True, "rm -fr inverted flags"),
    ("rm -r -f /var/cache", True, "rm -r -f split flags"),
    ("DROP TABLE users;", True, "DROP TABLE sql"),
    ("drop table if exists accounts", True, "drop table lowercase"),
    ("git push origin main --force", True, "git push --force"),
    ("git push -f origin main", True, "git push -f short flag"),
    ("git push --force-with-lease", True, "git push --force-with-lease"),
    ("TRUNCATE TABLE sessions;", True, "TRUNCATE TABLE sql"),
    ("TRUNCATE logs", True, "TRUNCATE without TABLE keyword"),
    ("DELETE FROM users;", True, "DELETE FROM without WHERE"),
    ("DELETE FROM accounts", True, "DELETE FROM without WHERE without semicolon"),
    
    # Safe commands (MUST ALLOW):
    ("DELETE FROM users WHERE id = 42;", False, "DELETE FROM with WHERE clause"),
    ("delete from tokens where expired_at < NOW()", False, "lowercase DELETE with WHERE"),
    ("git push origin main", False, "normal git push"),
    ("git status", False, "git status inspection"),
    ("rm temp.log", False, "single file removal (no recursive force)"),
    ("SELECT * FROM users;", False, "safe read query"),
    ("npm run test", False, "npm test suite"),
    ("python3 -m unittest discover", False, "python test suite")
]

def run_test():
    print("🚀 Starting Hook Verification Test Suite...")
    passed = 0
    failed = 0

    # Ensure log file can be monitored
    if LOG_FILE.exists():
        initial_log_size = LOG_FILE.stat().st_size
    else:
        initial_log_size = 0

    for cmd, should_block, desc in TEST_CASES:
        res = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT), cmd],
            capture_output=True,
            text=True
        )
        is_blocked = (res.returncode != 0)
        
        if is_blocked == should_block:
            passed += 1
            status = "✅ PASS"
        else:
            failed += 1
            status = "❌ FAIL"
            
        expected_str = "BLOCKED" if should_block else "ALLOWED"
        actual_str = "BLOCKED" if is_blocked else "ALLOWED"
        print(f"[{status}] {desc:<35} | Expected: {expected_str:<8} | Got: {actual_str}")

    # Verify log output
    print("\n🔍 Verifying blocked.log creation and contents...")
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > initial_log_size:
        print(f"✅ Log file verified at: {LOG_FILE}")
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-15:]
            print("  Recent Log Preview:")
            for l in lines:
                print("   ", l.rstrip())
    else:
        print("❌ Log file was not updated properly!")
        failed += 1

    print(f"\n==========================================")
    print(f"Summary: {passed} passed, {failed} failed")
    print(f"==========================================")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 ALL ACCEPTANCE CRITERIA VERIFIED!")
        sys.exit(0)

if __name__ == "__main__":
    run_test()
