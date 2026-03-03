#!/usr/bin/env python3
"""
Prepare inputs for the generate-mvp-document workflow.
Validates prerequisites and writes the manifest to 04-process/generate-mvp-document/manifest.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULTS = {
    "vc_pitch_file":   "05-outputs/generate-vc-pitch/vc-pitch-one-pager.md",
    "archetypes_file": "05-outputs/synthesise-archetypes/archetypes.md",
    "personas_dir":    "05-outputs/build-personas/personas",
    "brief_file":      "00-brief/strategic-research-brief.md",
    "template_file":   "10-resources/templates/mvp-brief-template.md",
    "manifest_file":   "04-process/generate-mvp-document/manifest.json",
    "output_file":     "05-outputs/generate-mvp-document/mvp-brief.md",
    # Section process files (written by specialist agents)
    "market_review_file":  "04-process/generate-mvp-document/market-review.md",
    "target_user_file":    "04-process/generate-mvp-document/target-user.md",
    "risks_file":          "04-process/generate-mvp-document/risks-constraints.md",
    "opportunity_file":    "04-process/generate-mvp-document/business-opportunity.md",
}


def check(path: str, label: str) -> bool:
    if not Path(path).exists():
        print(f"  MISSING  {label}: {path}")
        return False
    print(f"  OK       {label}: {path}")
    return True


def main():
    print("Phase: Prepare MVP Document Inputs")
    print("-" * 50)

    errors = []

    # --- Validate required inputs ---
    required = [
        (DEFAULTS["vc_pitch_file"],   "VC pitch one-pager"),
        (DEFAULTS["archetypes_file"], "Archetypes file"),
        (DEFAULTS["brief_file"],      "Strategic research brief"),
        (DEFAULTS["template_file"],   "MVP brief template"),
    ]

    for path, label in required:
        if not check(path, label):
            errors.append(f"Missing: {label} at {path}")

    # --- Validate personas directory ---
    personas_dir = Path(DEFAULTS["personas_dir"])
    if not personas_dir.exists():
        print(f"  MISSING  Personas directory: {personas_dir}")
        errors.append(f"Missing personas directory: {personas_dir}")
    else:
        persona_files = list(personas_dir.glob("*.md"))
        print(f"  OK       Personas directory: {personas_dir} ({len(persona_files)} files)")
        if not persona_files:
            errors.append("Personas directory exists but contains no .md files")

    if errors:
        print()
        for err in errors:
            print(f"FAIL  {err}")
        print("\nStatus: FAIL")
        sys.exit(1)

    # --- Write manifest ---
    manifest_path = Path(DEFAULTS["manifest_file"])
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "workflow":           "generate-mvp-document",
        "created_at":         datetime.now(timezone.utc).isoformat(),
        "vc_pitch_file":      DEFAULTS["vc_pitch_file"],
        "archetypes_file":    DEFAULTS["archetypes_file"],
        "personas_dir":       DEFAULTS["personas_dir"],
        "brief_file":         DEFAULTS["brief_file"],
        "template_file":      DEFAULTS["template_file"],
        "output_file":        DEFAULTS["output_file"],
        "market_review_file": DEFAULTS["market_review_file"],
        "target_user_file":   DEFAULTS["target_user_file"],
        "risks_file":         DEFAULTS["risks_file"],
        "opportunity_file":   DEFAULTS["opportunity_file"],
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  Manifest: {manifest_path}")
    print("\nStatus: PASS")


if __name__ == "__main__":
    main()
