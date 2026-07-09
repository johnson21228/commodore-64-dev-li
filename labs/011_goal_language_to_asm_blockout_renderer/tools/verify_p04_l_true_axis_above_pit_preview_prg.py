#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p04_l_true_axis_above_pit_preview.prg"
META = LAB / "dist" / "p04_l_true_axis_above_pit_preview_metadata.json"
errors=[]
for p in [PRG,META]:
    if not p.exists():
        errors.append(f"Missing required file: {p}")
if not errors:
    data=PRG.read_bytes()
    meta=json.loads(META.read_text(encoding="utf-8"))
    if data[:2] != bytes([0x01,0x08]): errors.append("PRG must load at $0801")
    if meta.get("pieceId") != "P04_L": errors.append("preview must use P04_L")
    if meta.get("shortcutRemoved") is not True: errors.append("shortcutRemoved must be true")
    if meta.get("abovePit") is not True: errors.append("abovePit must be true")
    if meta.get("floorDots") is not False: errors.append("floorDots must be false")
    controls=meta.get("axisControls",{})
    if controls != {"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"}:
        errors.append("axis controls must be true x/y/z controls")
    n=meta.get("orientationCount",0)
    if n < 8:
        errors.append("orientationCount should show more than the old four-state z shortcut")
    transitions=meta.get("transitions",{})
    if len(transitions) != n:
        errors.append("transition table must include every orientation")
    for idx,row in transitions.items():
        if set(row.keys()) != {"A","Q","S","W","D","E"}:
            errors.append(f"transition row {idx} must include all six axis keys")
    orientations=meta.get("orientations",{})
    if len(orientations) != n:
        errors.append("orientations table must include every orientation")
    for idx,row in orientations.items():
        if len(row.get("placedCells",[])) != 4:
            errors.append(f"orientation {idx} must place four cells")
        if row.get("whiteScreenCellCount",0) <= 0:
            errors.append(f"orientation {idx} must paint active cells white")
    if "transition table" not in meta.get("runtimeTruth",""):
        errors.append("runtimeTruth must describe transition table")
    if meta.get("runtimeStatefulRotation") is not True:
        errors.append("runtimeStatefulRotation must be true")
if errors:
    print("ERROR: P04_L true axis above-pit preview verification failed.")
    for e in errors: print(f"- {e}")
    raise SystemExit(1)
print("OK: P04_L true axis above-pit preview PRG verified.")
