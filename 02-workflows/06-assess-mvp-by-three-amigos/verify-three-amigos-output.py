#!/usr/bin/env python3
"""
Verify the Three Amigos assessment output for the assess-mvp-by-three-amigos workflow.
Checks: file exists, word count <= max, all required headings present, footer present,
recommendation count <= 5, transcript exists and has minimum message count.
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Executive Summary",
    "## Desirability Assessment",
    "## Feasibility Assessment",
    "## Viability Assessment",
    "## Cross-Cutting Tensions",
    "## Consensus Recommendations",
]

DEFAULT_MAX_WORDS = 2500
DEFAULT_MAX_RECOMMENDATIONS = 5
DEFAULT_MIN_TRANSCRIPT_MESSAGES = 6

TRANSCRIPT_PATH = "04-process/06-assess-mvp-by-three-amigos/discussion-transcript.md"


def count_words(text: str) -> int:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return len(text.split())


def check_footer(text: str):
    match = re.search(r"MVP Brief reviewed by Three Amigos panel", text, flags=re.IGNORECASE)
    return match is not None


def count_recommendations(text: str) -> int:
    """Count numbered items in the Consensus Recommendations section."""
    section_match = re.search(
        r"## Consensus Recommendations(.*?)(?=^##|\Z)",
        text, flags=re.MULTILINE | re.DOTALL
    )
    if not section_match:
        return 0
    section = section_match.group(1)
    # Count numbered list items (1. 2. etc.)
    numbered = re.findall(r"^\s*\d+\.", section, flags=re.MULTILINE)
    # Also count bullet points as fallback
    bullets = re.findall(r"^\s*[-*]", section, flags=re.MULTILINE)
    return max(len(numbered), len(bullets))


def count_transcript_messages(transcript_path: str) -> int:
    """Count the number of speaker messages in the discussion transcript."""
    path = Path(transcript_path)
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    # Messages are lines starting with **[Speaker Name]**
    messages = re.findall(r"^\*\*\[.+?\]\*\*", text, flags=re.MULTILINE)
    return len(messages)


def main():
    parser = argparse.ArgumentParser(description="Verify Three Amigos assessment output.")
    parser.add_argument("--file", required=True, help="Path to mvp-three-amigos-assessment.md")
    parser.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS)
    parser.add_argument("--max-recommendations", type=int, default=DEFAULT_MAX_RECOMMENDATIONS)
    parser.add_argument("--min-transcript-messages", type=int, default=DEFAULT_MIN_TRANSCRIPT_MESSAGES)
    parser.add_argument("--transcript", default=TRANSCRIPT_PATH)
    args = parser.parse_args()

    print("Phase: Verify Three Amigos Output")
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
    footer_ok = check_footer(text)
    rec_count = count_recommendations(text)
    msg_count = count_transcript_messages(args.transcript)

    print(f"  Output file : {args.file}")
    print(f"  Word count  : {word_count} / {args.max_words} max")
    print(f"  Recommendations: {rec_count} / {args.max_recommendations} max")
    print(f"  Transcript messages: {msg_count} / {args.min_transcript_messages} min")

    # --- Word count ---
    if word_count > args.max_words:
        errors.append(f"Word count {word_count} exceeds maximum {args.max_words}")

    # --- Required headings ---
    missing_headings = [h for h in REQUIRED_HEADINGS if h not in text]
    if missing_headings:
        for h in missing_headings:
            print(f"  MISSING heading: {h}")
            errors.append(f"Missing required heading: {h}")
    else:
        print(f"  Headings    : all {len(REQUIRED_HEADINGS)} present")

    # --- Footer ---
    if not footer_ok:
        print("  Footer      : MISSING")
        errors.append("Missing footer: 'MVP Brief reviewed by Three Amigos panel'")
    else:
        print("  Footer      : present")

    # --- Recommendation count ---
    if rec_count > args.max_recommendations:
        errors.append(f"Consensus Recommendations count {rec_count} exceeds maximum {args.max_recommendations}")

    # --- Transcript ---
    if msg_count < args.min_transcript_messages:
        errors.append(
            f"Discussion transcript has only {msg_count} messages "
            f"(minimum {args.min_transcript_messages} required for genuine back-and-forth)"
        )

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
