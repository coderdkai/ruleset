#!/usr/bin/env python3
"""
scripts/add_rule.py - Quick Rule Management CLI for RuleSet

Usage examples:
  python3 scripts/add_rule.py -r AI -d cursorapi.com
  python3 scripts/add_rule.py -r UnBan -t DOMAIN -d internal.example.com --push
  python3 scripts/add_rule.py -r ProxyGFW -d api.myproxy.org -m "My custom proxy" --push
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULESET_DIR = os.path.join(BASE_DIR, "Clash", "Ruleset")

VALID_TYPES = [
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
    "GEOIP",
    "GEOSITE",
]


def clean_target(raw_target: str, rule_type: str) -> str:
    """Clean domain/IP target to standard format."""
    target = raw_target.strip()
    if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
        if target.startswith("http://") or target.startswith("https://"):
            parsed = urlparse(target)
            target = parsed.hostname or target
        if "/" in target:
            target = target.split("/")[0]
        if ":" in target and not target.endswith("]"):  # Not IPv6
            target = target.split(":")[0]
    return target.strip()


def resolve_file(ruleset_name: str) -> str:
    if not ruleset_name.endswith(".list"):
        ruleset_name += ".list"
    file_path = os.path.join(RULESET_DIR, ruleset_name)
    if not os.path.exists(file_path):
        # Auto-create if not exists
        os.makedirs(RULESET_DIR, exist_ok=True)
        today = datetime.date.today().isoformat()
        stem = os.path.splitext(ruleset_name)[0]
        header = (
            f"# NAME: {stem}\n"
            f"# AUTHOR: coderdkai\n"
            f"# REPO: https://github.com/coderdkai/ruleset\n"
            f"# UPDATED: {today}\n"
            f"# DESCRIPTION: Custom {stem} Ruleset\n\n"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(header)
    return file_path


def update_date_in_content(content: str) -> str:
    today = datetime.date.today().isoformat()
    return re.sub(
        r"^# UPDATED:.*$",
        f"# UPDATED: {today}",
        content,
        flags=re.MULTILINE,
    )


def add_rule(
    ruleset: str,
    rule_type: str,
    target: str,
    comment: str | None = None,
    push: bool = False,
) -> bool:
    rule_type = rule_type.upper()
    if rule_type not in VALID_TYPES:
        print(f"[-] Invalid rule type '{rule_type}'. Valid types: {', '.join(VALID_TYPES)}")
        return False

    cleaned_target = clean_target(target, rule_type)
    if not cleaned_target:
        print("[-] Cleaned target is empty.")
        return False

    rule_line = f"{rule_type},{cleaned_target}"
    file_path = resolve_file(ruleset)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    # Check for duplicates
    for line in lines:
        stripped = line.strip()
        if stripped.split("#")[0].strip() == rule_line:
            print(f"[!] Rule '{rule_line}' already exists in {os.path.basename(file_path)}")
            return False

    # Append rule
    new_entry = rule_line
    if comment:
        new_entry += f" # {comment}"

    # Update date
    content = update_date_in_content(content)
    if not content.endswith("\n"):
        content += "\n"
    content += new_entry + "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Added '{new_entry}' -> {os.path.basename(file_path)}")

    if push:
        commit_and_push(ruleset, new_entry)

    return True


def commit_and_push(ruleset: str, entry: str):
    print("[*] Committing and pushing to git remote...")
    try:
        subprocess.run(
            ["git", "add", "."],
            cwd=BASE_DIR,
            check=True,
        )
        commit_msg = f"feat({ruleset}): add {entry.split('#')[0].strip()}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=BASE_DIR,
            check=True,
        )
        subprocess.run(
            ["git", "push"],
            cwd=BASE_DIR,
            check=True,
        )
        print("[+] Git push completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Git command failed: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Add rule to Clash Ruleset")
    parser.add_argument(
        "-r", "--ruleset",
        default="AI",
        help="Ruleset name without extension (e.g. AI, LinuxDo, ProxyGFW, UnBan). Default: AI",
    )
    parser.add_argument(
        "-t", "--type",
        default="DOMAIN-SUFFIX",
        help="Rule type (DOMAIN-SUFFIX, DOMAIN, DOMAIN-KEYWORD, IP-CIDR, etc.). Default: DOMAIN-SUFFIX",
    )
    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Domain or target string (URLs will be stripped to hostname)",
    )
    parser.add_argument(
        "-c", "--comment",
        default=None,
        help="Optional comment",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Auto git commit and git push upon modification",
    )

    args = parser.parse_args()
    success = add_rule(
        ruleset=args.ruleset,
        rule_type=args.type,
        target=args.domain,
        comment=args.comment,
        push=args.push,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
