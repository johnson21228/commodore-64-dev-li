#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p04_l_rotation_cycle_preview.prg"
META = LAB / "dist" / "p04_l_rotation_cycle_preview_metadata.json"

errors: list[str] = []
for path in [PRG, META]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")
    if meta.get("pieceId") != "P04_L":
        errors.append("preview must use existing P04_L piece")
    states = meta.get("states", {})
    if set(states.keys()) != {"0", "1", "2", "3"}:
        errors.append("P04_L preview must include four visible rotation states")
    for state_id, state in states.items():
        if len(state.get("occupiedCells", [])) != 4:
            errors.append(f"state {state_id} must have four occupied cells")
        if state.get("recordCount", 0) <= 0:
            errors.append(f"state {state_id} must have drawing records")

    if meta.get("cycle") != "0 -> 1 -> 2 -> 3 -> 0":
        errors.append("cycle must be a four-state loop")
    if meta.get("runtimeKeyboard") is not True:
        errors.append("runtimeKeyboard must be true")
    if meta.get("runtimeStatefulRotation") is not True:
        errors.append("runtimeStatefulRotation must be true")
    if meta.get("previewOnly") is not True:
        errors.append("previewOnly must be true")

if errors:
    print("ERROR: P04_L rotation-cycle preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P04_L four-state rotation-cycle preview PRG verified.")
