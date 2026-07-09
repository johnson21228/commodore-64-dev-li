#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p04_l_true_axis_endpoint_3x3_pit_preview.prg"
META = LAB / "dist" / "p04_l_true_axis_endpoint_3x3_pit_preview_metadata.json"
REPORT = LAB / "dist" / "pieces" / "P04_L.true_axis_endpoint_3x3_pit_payload_report.json"

errors: list[str] = []

for path in [PRG, META, REPORT]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")
    if len(data) != 30719:
        errors.append("PRG image should be fixed lab image size 30719 bytes")
    if meta.get("pieceId") != "P04_L":
        errors.append("preview must be for P04_L")
    if meta.get("mode") != "true-axis endpoint 3x3 pit preview":
        errors.append("wrong preview mode")
    if meta.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("pitDimensions must be 3x3x10")
    if meta.get("shortcutRemoved") is not True:
        errors.append("shortcutRemoved must be true")
    if meta.get("abovePit") is not True:
        errors.append("abovePit must be true")
    if meta.get("axisControls") != {"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"}:
        errors.append("axis controls must be true x/y/z controls")
    if meta.get("orientationCount") != 24:
        errors.append("orientationCount must be 24")
    if meta.get("runtimeLineDrawing") is not True:
        errors.append("runtimeLineDrawing must be true")
    if meta.get("floorDots") is not False:
        errors.append("floorDots must be false")
    if "3x3x10" not in meta.get("pitStyle", ""):
        errors.append("pitStyle must name 3x3x10 pit")
    sizes = meta.get("sizes", {})
    if sizes.get("pitRecordBytes", 0) <= 138:
        errors.append("3x3 pit should have more pit record bytes than the first sparse endpoint preview")
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("program must fit within available PRG image bytes")
    if report.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("source endpoint report must be 3x3x10")
    if report.get("summary", {}).get("classification") == "CONFLICT":
        errors.append("source endpoint report must not be CONFLICT")

if errors:
    print("ERROR: P04_L true-axis endpoint 3x3 pit preview PRG verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P04_L true-axis endpoint 3x3 pit preview PRG verified.")
