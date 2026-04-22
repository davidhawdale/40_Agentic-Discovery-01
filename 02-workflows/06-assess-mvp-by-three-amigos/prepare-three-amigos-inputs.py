#!/usr/bin/env python3
"""
Prepare inputs for the assess-mvp-by-three-amigos workflow.
Validates prerequisites, creates working directories, writes manifest.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULTS = {
    "mvp_brief_file":     "05-outputs/04-generate-mvp-document/mvp-brief.md",
    "strategic_brief_file": "00-brief/strategic-research-brief.md",
    "template_file":      "10-resources/templates/three-amigos-output-template.md",
    "manifest_file":      "04-process/06-assess-mvp-by-three-amigos/manifest.json",
    "phase1_dir":         "04-process/06-assess-mvp-by-three-amigos/phase1-reviews",
    "phase2_dir":         "04-process/06-assess-mvp-by-three-amigos/phase2-discussion",
    "transcript_file":    "04-process/06-assess-mvp-by-three-amigos/discussion-transcript.md",
    "output_file":        "05-outputs/06-assess-mvp-by-three-amigos/mvp-three-amigos-assessment.md",
}


def check(path: str, label: str) -> bool:
    if not Path(path).exists():
        print(f"  MISSING  {label}: {path}")
        return False
    print(f"  OK       {label}: {path}")
    return True


def main():
    print("Phase: Prepare Three Amigos Inputs")
    print("-" * 50)

    errors = []

    # --- Validate required inputs ---
    required = [
        (DEFAULTS["mvp_brief_file"],      "MVP brief"),
        (DEFAULTS["strategic_brief_file"], "Strategic research brief"),
        (DEFAULTS["template_file"],        "Output template"),
    ]

    for path, label in required:
        if not check(path, label):
            errors.append(f"Missing: {label} at {path}")

    if errors:
        print()
        for err in errors:
            print(f"FAIL  {err}")
        print("\nStatus: FAIL")
        sys.exit(1)

    # --- Create working directories ---
    for key in ("phase1_dir", "phase2_dir"):
        d = Path(DEFAULTS[key])
        d.mkdir(parents=True, exist_ok=True)
        print(f"  DIR      {d}")

    # --- Create output directory ---
    Path(DEFAULTS["output_file"]).parent.mkdir(parents=True, exist_ok=True)

    # --- Write manifest ---
    manifest_path = Path(DEFAULTS["manifest_file"])
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "workflow":            "assess-mvp-by-three-amigos",
        "created_at":          datetime.now(timezone.utc).isoformat(),
        "mvp_brief_file":      DEFAULTS["mvp_brief_file"],
        "strategic_brief_file": DEFAULTS["strategic_brief_file"],
        "template_file":       DEFAULTS["template_file"],
        "phase1_dir":          DEFAULTS["phase1_dir"],
        "phase2_dir":          DEFAULTS["phase2_dir"],
        "transcript_file":     DEFAULTS["transcript_file"],
        "output_file":         DEFAULTS["output_file"],
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  Manifest: {manifest_path}")
    print("\nStatus: PASS")


if __name__ == "__main__":
    main()
