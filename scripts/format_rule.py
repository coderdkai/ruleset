#!/usr/bin/env python3
"""
scripts/format_rule.py - Deduplicate, format, and sort rule lists.
"""

import datetime
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULESET_DIR = os.path.join(BASE_DIR, "Clash", "Ruleset")


def format_ruleset_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    header_lines = []
    rule_entries = []
    is_header = True

    for line in lines:
        stripped = line.strip()
        if is_header and (stripped.startswith("#") or not stripped):
            header_lines.append(line)
        else:
            is_header = False
            if stripped and not stripped.startswith("#"):
                rule_entries.append(stripped)

    # Deduplicate while preserving order or sorting
    seen = set()
    deduped = []
    for entry in rule_entries:
        key = entry.split("#")[0].strip()
        if key and key not in seen:
            seen.add(key)
            deduped.append(entry)

    # Sort rules alphabetically
    deduped.sort()

    today = datetime.date.today().isoformat()
    new_header = []
    for h in header_lines:
        if h.startswith("# UPDATED:"):
            new_header.append(f"# UPDATED: {today}")
        else:
            new_header.append(h)

    # Reassemble
    result = "\n".join(new_header).strip() + "\n\n" + "\n".join(deduped) + "\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"[+] Formatted & deduped: {os.path.basename(file_path)} ({len(deduped)} rules)")


def main():
    if not os.path.exists(RULESET_DIR):
        print(f"[-] {RULESET_DIR} not found.")
        sys.exit(1)

    for item in os.listdir(RULESET_DIR):
        if item.endswith(".list"):
            format_ruleset_file(os.path.join(RULESET_DIR, item))


if __name__ == "__main__":
    main()
