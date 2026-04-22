#!/usr/bin/env python3
"""Prepare deterministic inputs for generate-vc-pitch.

Writes a manifest used by orchestration and vc-pitch-writer.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXTRACTS = ROOT / "04-process" / "synthesise-archetypes" / "extracts"
DEFAULT_BRIEF = ROOT / "00-brief" / "strategic-research-brief.md"
DEFAULT_TEMPLATE = ROOT / "10-resources" / "templates" / "vc-pitch-output-template.md"
DEFAULT_MANIFEST = ROOT / "04-process" / "generate-vc-pitch" / "manifest.json"
DEFAULT_OUTPUT = ROOT / "05-outputs" / "generate-vc-pitch" / "vc-pitch-one-pager.md"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare VC pitch workflow inputs")
    parser.add_argument("--extracts-dir", default=str(DEFAULT_EXTRACTS))
    parser.add_argument("--brief", default=str(DEFAULT_BRIEF))
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--out-manifest", default=str(DEFAULT_MANIFEST))
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    extracts_dir = Path(args.extracts_dir).resolve()
    brief_file = Path(args.brief).resolve()
    template_file = Path(args.template).resolve()
    out_manifest = Path(args.out_manifest).resolve()

    errors: list[str] = []

    if not brief_file.exists():
        errors.append(f"Strategic brief missing: {brief_file}")
    if not template_file.exists():
        errors.append(f"Template missing: {template_file}")
    if not extracts_dir.exists() or not extracts_dir.is_dir():
        errors.append(f"Extracts folder missing: {extracts_dir}")

    files: list[Path] = []
    if not errors:
        files = sorted(extracts_dir.glob("*.md"))
        if not files:
            errors.append(f"No extract files found in: {extracts_dir}")

    if errors:
        print("\nPhase: Prepare VC Pitch Inputs")
        print("-" * 50)
        for err in errors:
            print(f"FAIL  {err}")
        print("\nStatus: FAIL")
        return 1

    manifest = {
        "workflow": "generate-vc-pitch",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "extracts_dir": rel(extracts_dir),
        "brief_file": rel(brief_file),
        "template_file": rel(template_file),
        "output_file": rel(DEFAULT_OUTPUT),
        "files": [rel(p) for p in files],
        "summary": {
            "total_extracts": len(files),
        },
    }

    out_manifest.parent.mkdir(parents=True, exist_ok=True)
    out_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print("\nPhase: Prepare VC Pitch Inputs")
    print("-" * 50)
    print(f"  Extracts folder : {rel(extracts_dir)}")
    print(f"  Extract files   : {len(files)}")
    print(f"  Brief file      : {rel(brief_file)}")
    print(f"  Template file   : {rel(template_file)}")
    print(f"  Manifest        : {rel(out_manifest)}")
    print("\nStatus: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
