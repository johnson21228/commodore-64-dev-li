#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p02_domino_rotation_cycle_keys_preview.prg"
META = LAB / "dist" / "p02_domino_rotation_cycle_keys_preview_metadata.json"

errors: list[str] = []
for path in [PRG, META]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))
    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")

    for key in ["A", "Q", "S", "W", "D", "E"]:
        if key not in meta.get("controls", {}):
            errors.append(f"Missing key control: {key}")

    states = meta.get("states", {})
    if set(states.keys()) != {"0", "1", "2"}:
        errors.append("stateful preview must include three domino visible states")
    for state_id, expected_name in [("0", "x_axis"), ("1", "y_axis"), ("2", "z_axis")]:
        if states.get(state_id, {}).get("name") != expected_name:
            errors.append(f"state {state_id} must be {expected_name}")

    if meta.get("runtimeStatefulRotation") is not True:
        errors.append("runtimeStatefulRotation must be true")
    if meta.get("runtimeKeyboard") is not True:
        errors.append("runtimeKeyboard must be true")
    if meta.get("previewOnly") is not True:
        errors.append("previewOnly must be true")
    transition_text = " ".join(meta.get("transitionModel", {}).keys())
    if "x-axis rotation" not in transition_text or "y-axis rotation" not in transition_text or "z-axis rotation" not in transition_text:
        errors.append("transition model must describe x/y/z axis rotation")

if errors:
    print("ERROR: P02_DOMINO rotation-cycle keys preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P02_DOMINO stateful rotation-cycle keys preview PRG verified.")
