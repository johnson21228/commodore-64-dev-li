#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p03_elbow_true_axis_endpoint_3x3_green_line_pit_preview.prg"
META = LAB / "dist" / "p03_elbow_true_axis_endpoint_3x3_green_line_pit_preview_metadata.json"
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"

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
    if meta.get("pieceId") != "P03_ELBOW":
        errors.append("preview must be for P03_ELBOW")
    if meta.get("mode") != "P03_ELBOW true-axis endpoint 3x3 green-line pit preview":
        errors.append("wrong preview mode")
    if meta.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("pitDimensions must be 3x3x10")
    if meta.get("maxBlockFootprintWidth") != 2:
        errors.append("maxBlockFootprintWidth must be 2")
    if meta.get("axisControls") != {"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"}:
        errors.append("axis controls must be true x/y/z controls")
    if meta.get("runtimeLineDrawing") is not True:
        errors.append("runtimeLineDrawing must be true")
    if meta.get("floorLines") is not False:
        errors.append("floorLines must be false")
    if "green" not in meta.get("pitStyle", "") or "grid lines" not in meta.get("pitStyle", ""):
        errors.append("pitStyle must describe green grid lines")
    sizes = meta.get("sizes", {})
    if sizes.get("pitRecordBytes", 0) <= 138:
        errors.append("green line pit should have more pit record bytes than sparse-dot preview")
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("program must fit within available PRG image bytes")
    if report.get("pieceId") != "P03_ELBOW":
        errors.append("source report must be P03_ELBOW")
    if report.get("summary", {}).get("classification") == "CONFLICT":
        errors.append("source endpoint report must not be CONFLICT")

if errors:
    print("ERROR: P03_ELBOW true-axis endpoint 3x3 green-line pit preview PRG verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW true-axis endpoint 3x3 green-line pit preview PRG verified.")
