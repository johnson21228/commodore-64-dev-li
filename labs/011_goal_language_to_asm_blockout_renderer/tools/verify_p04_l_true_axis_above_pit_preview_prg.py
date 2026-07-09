#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p04_l_true_axis_above_pit_preview.prg"
META = LAB / "dist" / "p04_l_true_axis_above_pit_preview_metadata.json"
CONFLICT = LAB / "dist" / "p04_l_true_axis_above_pit_preview_payload_conflict.json"

errors: list[str] = []

if PRG.exists() or META.exists():
    if not PRG.exists():
        errors.append(f"Missing required file: {PRG}")
    if not META.exists():
        errors.append(f"Missing required file: {META}")
    if not errors:
        data = PRG.read_bytes()
        meta = json.loads(META.read_text(encoding="utf-8"))
        if data[:2] != bytes([0x01, 0x08]):
            errors.append("PRG must load at $0801")
        if meta.get("pieceId") != "P04_L":
            errors.append("preview must use P04_L")
        if meta.get("shortcutRemoved") is not True:
            errors.append("shortcutRemoved must be true")
        if meta.get("abovePit") is not True:
            errors.append("abovePit must be true")
        if meta.get("floorDots") is not False:
            errors.append("floorDots must be false")
else:
    if not CONFLICT.exists():
        errors.append(f"Missing PRG/META and missing conflict report: {CONFLICT}")
    else:
        conflict = json.loads(CONFLICT.read_text(encoding="utf-8"))
        if conflict.get("pieceId") != "P04_L":
            errors.append("conflict report must be for P04_L")
        if conflict.get("result") != "CONFLICT":
            errors.append("conflict report result must be CONFLICT")
        if conflict.get("orientationCount", 0) < 8:
            errors.append("conflict report must show true-axis orientation expansion")
        if conflict.get("observedProgramBytes", 0) <= conflict.get("availablePrgImageBytes", 0):
            errors.append("conflict report must show observed bytes exceeding budget")
        if "endpoint" not in conflict.get("nextMove", ""):
            errors.append("conflict report must name endpoint/line-command next move")

if errors:
    print("ERROR: P04_L true axis above-pit preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

if CONFLICT.exists() and not PRG.exists():
    print("OK: P04_L true-axis full-bitmap preview verified as payload CONFLICT.")
else:
    print("OK: P04_L true axis above-pit preview PRG verified.")
