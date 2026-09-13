#!/usr/bin/env python3
"""
scripts/format_rule.py - Deduplicate, format, and section-sort rule lists.
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
    sections = []  # list of tuples: (section_title, [rule_lines])
    current_section_title = None
    current_section_rules = []
    is_header = True

    for line in lines:
        stripped = line.strip()
        if is_header:
            if stripped.startswith("# ---") or stripped.startswith("# ==="):
                is_header = False
                current_section_title = stripped
                current_section_rules = []
            elif stripped.startswith("#") or not stripped:
                header_lines.append(line)
            else:
                is_header = False
                current_section_rules.append(stripped)
        else:
            if stripped.startswith("# ---") or stripped.startswith("# ==="):
                if current_section_title or current_section_rules:
                    sections.append((current_section_title, current_section_rules))
                current_section_title = stripped
                current_section_rules = []
            elif stripped and not stripped.startswith("#"):
                current_section_rules.append(stripped)

    if current_section_title or current_section_rules:
        sections.append((current_section_title, current_section_rules))

    # Update date in header
    today = datetime.date.today().isoformat()
    new_header = []
    for h in header_lines:
        if h.startswith("# UPDATED:"):
            new_header.append(f"# UPDATED: {today}")
        else:
            new_header.append(h)

    # Global deduplication across sections
    seen = set()
    output_body = []
    total_rules = 0

    for sec_title, rules in sections:
        sec_deduped = []
        for r in rules:
            key = r.split("#")[0].strip()
            if key and key not in seen:
                seen.add(key)
                sec_deduped.append(r)
        sec_deduped.sort()
        total_rules += len(sec_deduped)

        if sec_title:
            output_body.append("")
            output_body.append(sec_title)
        output_body.extend(sec_deduped)

    result = "\n".join(new_header).strip() + "\n" + "\n".join(output_body).strip() + "\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"[+] Formatted & section-deduped: {os.path.basename(file_path)} ({total_rules} rules)")


def main():
    if not os.path.exists(RULESET_DIR):
        print(f"[-] {RULESET_DIR} not found.")
        sys.exit(1)

    for item in sorted(os.listdir(RULESET_DIR)):
        if item.endswith(".list"):
            format_ruleset_file(os.path.join(RULESET_DIR, item))


if __name__ == "__main__":
    main()
