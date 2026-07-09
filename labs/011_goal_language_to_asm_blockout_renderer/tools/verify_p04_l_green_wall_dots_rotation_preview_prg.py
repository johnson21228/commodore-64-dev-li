#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p04_l_green_wall_dots_rotation_preview.prg"
META = LAB / "dist" / "p04_l_green_wall_dots_rotation_preview_metadata.json"
errors=[]
for p in [PRG,META]:
    if not p.exists(): errors.append(f"Missing required file: {p}")
if not errors:
    data=PRG.read_bytes()
    meta=json.loads(META.read_text(encoding="utf-8"))
    if data[:2] != bytes([0x01,0x08]): errors.append("PRG must load at $0801")
    if meta.get("pieceId") != "P04_L": errors.append("preview must use P04_L")
    if "green dots" not in meta.get("pitStyle",""): errors.append("pitStyle must be green dots")
    if meta.get("floorDots") is not False: errors.append("floorDots must be false")
    if "default green" not in meta.get("colorStrategy",""): errors.append("colorStrategy must default to green")
    states=meta.get("states",{})
    if set(states.keys()) != {"0","1","2","3"}: errors.append("must include four states")
    for state in states.values():
        if state.get("whiteScreenCellCount",0) <= 0: errors.append("each state must mark active cells white")
    if meta.get("runtimeStatefulRotation") is not True: errors.append("runtimeStatefulRotation must be true")
    if meta.get("previewOnly") is not True: errors.append("previewOnly must be true")
if errors:
    print("ERROR: P04_L green wall-dot pit preview verification failed.")
    for e in errors: print(f"- {e}")
    raise SystemExit(1)
print("OK: P04_L green wall-dot pit rotation preview PRG verified.")
