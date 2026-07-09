#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p02_domino_full_rotation_keys_preview.prg"
META = LAB / "dist" / "p02_domino_full_rotation_keys_preview_metadata.json"

errors: list[str] = []
for path in [PRG, META]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")

    controls = meta.get("controls", {})
    for key in ["A", "Q", "S", "W", "D", "E"]:
        if key not in controls:
            errors.append(f"Missing rotation key: {key}")

    orientations = meta.get("orientations", {})
    for orientation in ["x_axis", "y_axis", "z_axis"]:
        if orientation not in orientations:
            errors.append(f"Missing orientation: {orientation}")
        elif orientations[orientation].get("recordCount", 0) <= 0:
            errors.append(f"{orientation} must have drawing records")

    if orientations.get("z_axis", {}).get("occupiedCells") != [[2, 2, 0], [2, 2, 1]] and orientations.get("z_axis", {}).get("occupiedCells") != [(2, 2, 0), (2, 2, 1)]:
        errors.append("z_axis must be the depth orientation")

    if meta.get("runtimeKeyboard") is not True:
        errors.append("preview must have runtimeKeyboard=true")
    if meta.get("runtimeLineDrawing") is not False:
        errors.append("this ASAP preview must not claim runtime line drawing")
    if meta.get("previewOnly") is not True:
        errors.append("previewOnly must be true")

    if len(data) != 0x8000 - 0x0801:
        errors.append("PRG memory image should run to $8000 for bitmap preview")

if errors:
    print("ERROR: P02_DOMINO full rotation keys preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P02_DOMINO full rotation keys preview PRG verified.")
