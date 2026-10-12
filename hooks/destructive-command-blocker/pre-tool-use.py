#!/usr/bin/env python3
"""
Claude Code Pre-Tool-Use Hook: Destructive Command Blocker
Blocks dangerous bash commands (rm -rf, DROP TABLE, git push --force, TRUNCATE, DELETE FROM without WHERE)
and logs attempts to ~/.claude/hooks/blocked.log.
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path

# Log file destination
HOOKS_DIR = Path.home() / ".claude" / "hooks"
LOG_FILE = HOOKS_DIR / "blocked.log"

# Rules definition: (regex pattern, description)
BLOCKED_PATTERNS = [
    # 1. rm -rf variants (rm -rf, rm -fr, rm -r -f, rm --recursive --force, etc.)
    (
        re.compile(
            r"\brm\s+.*?(?:-[a-zA-Z]*[rf][a-zA-Z]*|--recursive\s+--force|--force\s+--recursive|-r\s+--force|--force\s+-r)\b",
            re.IGNORECASE
        ),
        "Recursive force removal ('rm -rf') detected. High risk of irrecoverable data loss."
    ),
    # 2. DROP TABLE / DROP DATABASE (case-insensitive SQL)
    (
        re.compile(r"\bDROP\s+(?:TABLE|DATABASE|SCHEMA)\b", re.IGNORECASE),
        "Database destructive command ('DROP TABLE/DATABASE') detected."
    ),
    # 3. git push --force (or git push -f, --force-with-lease, +branch)
    (
        re.compile(r"\bgit\s+push\b.*?\s+(?:--force|-f\b|--force-with-lease\b|\+\w+)", re.IGNORECASE),
        "Remote repository history rewrite ('git push --force') detected."
    ),
    # 4. TRUNCATE (SQL TRUNCATE / TRUNCATE TABLE)
    (
        re.compile(r"\bTRUNCATE(?:\s+TABLE)?\s+[a-zA-Z0-9_`\"']+", re.IGNORECASE),
        "Database table purge ('TRUNCATE') detected."
    ),
    # 5. DELETE FROM without WHERE clause
    (
        re.compile(r"\bDELETE\s+FROM\s+[a-zA-Z0-9_`\"']+(?!\s+WHERE\b)[^;]*;?", re.IGNORECASE),
        "Unbounded table deletion ('DELETE FROM' without WHERE clause) detected."
    )
]

def check_delete_from_without_where(cmd: str) -> bool:
    """Special check for DELETE FROM lacking a WHERE clause across multi-line or chained commands."""
    delete_matches = re.finditer(r"\bDELETE\s+FROM\s+([a-zA-Z0-9_`\"']+)([^;]*)(?:;|$)", cmd, re.IGNORECASE)
    for m in delete_matches:
        clause = m.group(2)
        if not re.search(r"\bWHERE\b", clause, re.IGNORECASE):
            return True
    return False

def check_command(cmd: str) -> tuple[bool, str]:
    """Returns (is_blocked, reason)"""
    # Check general patterns
    for pattern, reason in BLOCKED_PATTERNS[:4]:
        if pattern.search(cmd):
            return True, reason
            
    # Check DELETE FROM without WHERE
    if check_delete_from_without_where(cmd):
        return True, "Unbounded table deletion ('DELETE FROM' without WHERE clause) detected."
        
    return False, ""

def log_blocked_command(cmd: str, cwd: str, reason: str):
    """Logs blocked attempt to ~/.claude/hooks/blocked.log with timestamp, command, and cwd."""
    try:
        HOOKS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().isoformat()
        log_entry = (
            f"[{timestamp}] BLOCKED\n"
            f"  Command:      {cmd.strip()}\n"
            f"  Project Path: {cwd}\n"
            f"  Reason:       {reason}\n"
            f"{'-' * 60}\n"
        )
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        sys.stderr.write(f"[pre-tool-use-hook] Warning: Could not write to log: {e}\n")

def main():
    # Detect command from CLI argument or stdin JSON (Claude Code hook protocols)
    cmd = ""
    cwd = os.getcwd()
    
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
    else:
        # Check stdin for JSON payload or raw command
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read().strip()
            if raw_input:
                try:
                    payload = json.loads(raw_input)
                    if isinstance(payload, dict):
                        # Extract command from standard hook payload
                        cmd = payload.get("command") or payload.get("tool_input", {}).get("command") or raw_input
                        cwd = payload.get("cwd") or payload.get("tool_input", {}).get("cwd") or cwd
                    else:
                        cmd = raw_input
                except Exception:
                    cmd = raw_input

    if not cmd:
        sys.exit(0)

    is_blocked, reason = check_command(cmd)
    if is_blocked:
        log_blocked_command(cmd, cwd, reason)
        sys.stderr.write(
            f"\n🚨 [BLOCKED BY CLAUDE HOOK] Destructive Command Intercepted!\n"
            f"Reason: {reason}\n"
            f"Command: {cmd}\n"
            f"Action: Execution halted. Modification logged to {LOG_FILE}\n\n"
        )
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
