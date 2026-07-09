#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p02_domino_top_endpoint_preview.prg"
META = LAB / "dist" / "p02_domino_top_endpoint_preview_metadata.json"
REPORT = LAB / "dist" / "pieces" / "P02_DOMINO.endpoint_payload_report.json"

errors: list[str] = []

for path in [PRG, META, REPORT]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    meta = json.loads(META.read_text(encoding="utf-8"))
    data = PRG.read_bytes()

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")

    selected = meta.get("selectedPose", {})
    if selected.get("pieceId") != "P02_DOMINO":
        errors.append("selected pose must be P02_DOMINO")
    if selected.get("rotationId") != "x_axis":
        errors.append("selected rotation must be x_axis")
    if selected.get("z") != 0:
        errors.append("selected pose must start at top level z=0")
    if selected.get("x") != 1 or selected.get("y") != 2:
        errors.append("selected pose must be centered-ish at x=1, y=2")

    if meta.get("runtimeLineDrawing") is not False:
        errors.append("this preview must not claim runtime line drawing yet")
    if meta.get("previewOnly") is not True:
        errors.append("metadata previewOnly must be true")

    if meta.get("blockTouchedCells", 0) <= 0:
        errors.append("active block must touch at least one color cell")
    if meta.get("pitTouchedCells", 0) <= 0:
        errors.append("pit must touch color cells")

    if len(data) < 0x7000:
        errors.append("PRG should include bitmap/screen memory image")

if errors:
    print("ERROR: P02_DOMINO top endpoint preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P02_DOMINO top-level endpoint preview PRG verified.")
