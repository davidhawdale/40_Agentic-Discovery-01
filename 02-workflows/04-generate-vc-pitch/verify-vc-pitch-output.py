#!/usr/bin/env python3
"""Verify output quality gates for generate-vc-pitch."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FILE = ROOT / "05-outputs" / "generate-vc-pitch" / "vc-pitch-one-pager.md"
DEFAULT_EXTRACTS = ROOT / "04-process" / "synthesise-archetypes" / "extracts"
REQUIRED_HEADINGS = [
    "## The Problem",
    "## What Users Actually Want",
    "## The Opportunity",
    "## What \"Trustworthy\" Means",
    "## Our Positioning",
]


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify VC pitch output")
    parser.add_argument("--file", default=str(DEFAULT_FILE))
    parser.add_argument("--extracts-dir", default=str(DEFAULT_EXTRACTS))
    parser.add_argument("--max-words", type=int, default=600)
    return parser.parse_args()


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def parse_interview_count(text: str) -> int | None:
    match = re.search(r"Based on\s*\[(\d+)\]\s*interview transcripts", text, flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1))


def main() -> int:
    args = parse_args()
    output_file = Path(args.file).resolve()
    extracts_dir = Path(args.extracts_dir).resolve()

    errors: list[str] = []

    if not extracts_dir.exists() or not extracts_dir.is_dir():
        errors.append(f"Extracts folder missing: {extracts_dir}")
        extract_count = 0
    else:
        extract_count = len(list(extracts_dir.glob("*.md")))
        if extract_count == 0:
            errors.append(f"No extract files found in: {extracts_dir}")

    if not output_file.exists():
        errors.append(f"Output file missing: {output_file}")
        text = ""
    else:
        text = output_file.read_text(encoding="utf-8")

    if text:
        word_count = count_words(text)
        if word_count > args.max_words:
            errors.append(f"Word count too high: {word_count} > {args.max_words}")

        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"Missing required heading: {heading}")

        footer_count = parse_interview_count(text)
        if footer_count is None:
            errors.append("Missing footer interview count: 'Based on [N] interview transcripts'")
        elif extract_count and footer_count != extract_count:
            errors.append(f"Interview count mismatch: footer={footer_count}, extracts={extract_count}")
    else:
        word_count = 0
        footer_count = None

    print("\nPhase: Verify VC Pitch Output")
    print("-" * 50)
    print(f"  Output file      : {output_file if not output_file.exists() else rel(output_file)}")
    print(f"  Extracts dir     : {extracts_dir if not extracts_dir.exists() else rel(extracts_dir)}")
    print(f"  Extract count    : {extract_count}")
    print(f"  Word count       : {word_count}")
    print(f"  Footer interviews: {footer_count if footer_count is not None else 'MISSING'}")

    if errors:
        for err in errors:
            print(f"FAIL  {err}")
        print("\nStatus: FAIL")
        return 1

    print("\nStatus: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
