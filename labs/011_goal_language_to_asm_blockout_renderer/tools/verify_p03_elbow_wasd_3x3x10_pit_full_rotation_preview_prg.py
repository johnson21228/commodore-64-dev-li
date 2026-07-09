#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_full_rotation_preview.prg"
META = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_full_rotation_preview_metadata.json"
BUILDER = LAB / "tools" / "build_p03_elbow_wasd_3x3x10_pit_full_rotation_preview_prg.py"
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"

errors = []
for path in [PRG, META, BUILDER, REPORT]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))
    builder = BUILDER.read_text(encoding="utf-8")
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")
    if len(data) != 30719:
        errors.append("PRG image should be fixed lab image size 30719 bytes")
    if meta.get("pieceId") != "P03_ELBOW":
        errors.append("preview must be for P03_ELBOW")
    if meta.get("mode") != "P03_ELBOW WASD 3x3x10 pit full-rotation preview":
        errors.append("wrong mode")
    if meta.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("pitDimensions must be 3x3x10")
    if meta.get("maxBlockFootprintWidth") != 2:
        errors.append("maxBlockFootprintWidth must be 2")
    if meta.get("orientationCount") != 12:
        errors.append("P03_ELBOW must have 12 orientations")
    if meta.get("axisControls") != {"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"}:
        errors.append("axis controls must be true x/y/z controls")
    if meta.get("runtimeLineDrawing") is not True:
        errors.append("runtimeLineDrawing must be true for block endpoints")
    if "WASD" not in meta.get("pitStyle", ""):
        errors.append("pitStyle must identify WASD known-good pit")
    if "PIT_W = 3" not in builder or "PIT_H = 3" not in builder:
        errors.append("builder must set WASD pit to 3x3")
    if "PIT_VISUAL_DEPTH = 10" not in builder:
        errors.append("builder must preserve depth 10")
    sizes = meta.get("sizes", {})
    if sizes.get("pitRecordBytes", 0) <= 1000:
        errors.append("WASD pit should have substantial compact pit records")
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("program must fit within available PRG image bytes")
    if report.get("pieceId") != "P03_ELBOW" or report.get("orientationCount") != 12:
        errors.append("source endpoint report must be P03_ELBOW with 12 orientations")

if errors:
    print("ERROR: P03_ELBOW WASD 3x3x10 pit full-rotation preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW WASD 3x3x10 pit full-rotation preview verified.")
