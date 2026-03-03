#!/usr/bin/env python3
"""
Verify the MVP brief output for the generate-mvp-document workflow.
Checks: file exists, word count <= max, all required headings present, footer present.
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Problem Statement",
    "## Scope",
    "## Target User",
    "## Experiments",
    "## Risks and Constraints",
    "## Market Review",
    "## Opportunity Statement",
]

DEFAULT_MAX_WORDS = 2500


def count_words(text: str) -> int:
    # Strip markdown comment blocks before counting
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return len(text.split())


def check_footer(text: str):
    match = re.search(r"Based on\s*\[(\d+)\]\s*interview transcripts", text, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def main():
    parser = argparse.ArgumentParser(description="Verify MVP brief output.")
    parser.add_argument("--file", required=True, help="Path to mvp-brief.md")
    parser.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS)
    args = parser.parse_args()

    print("Phase: Verify MVP Brief Output")
    print("-" * 50)

    errors = []
    path = Path(args.file)

    # --- File exists ---
    if not path.exists():
        print(f"  Output file : MISSING ({args.file})")
        print("\nStatus: FAIL")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    word_count = count_words(text)
    footer_count = check_footer(text)

    print(f"  Output file : {args.file}")
    print(f"  Word count  : {word_count} / {args.max_words} max")

    # --- Word count ---
    if word_count > args.max_words:
        errors.append(f"Word count {word_count} exceeds maximum {args.max_words}")

    # --- Required headings ---
    missing_headings = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            missing_headings.append(heading)

    if missing_headings:
        for h in missing_headings:
            print(f"  MISSING heading: {h}")
            errors.append(f"Missing required heading: {h}")
    else:
        print(f"  Headings    : all {len(REQUIRED_HEADINGS)} present")

    # --- Footer ---
    if footer_count is None:
        print("  Footer      : MISSING")
        errors.append("Missing footer: 'Based on [N] interview transcripts and market data'")
    else:
        print(f"  Footer      : [{footer_count}] interviews")

    # --- Result ---
    print()
    if errors:
        for err in errors:
            print(f"FAIL  {err}")
        print("\nStatus: FAIL")
        sys.exit(1)
    else:
        print("Status: PASS")


if __name__ == "__main__":
    main()
