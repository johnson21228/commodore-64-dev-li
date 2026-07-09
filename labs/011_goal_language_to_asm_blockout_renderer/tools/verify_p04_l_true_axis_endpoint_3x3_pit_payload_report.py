#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P04_L.true_axis_endpoint_3x3_pit_payload_report.json"
CONFLICT = LAB / "dist" / "p04_l_true_axis_above_pit_preview_payload_conflict.json"

errors: list[str] = []

if not REPORT.exists():
    errors.append(f"Missing report: {REPORT}")
else:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("pieceId") != "P04_L":
        errors.append("report must be for P04_L")
    if report.get("reportType") != "true-axis endpoint 3x3 pit payload report":
        errors.append("wrong reportType")
    if report.get("orientationCount") != 24:
        errors.append("P04_L true-axis report must have 24 orientations")
    if report.get("axisControls") != {"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"}:
        errors.append("axis controls must be true x/y/z controls")
    if report.get("abovePit") is not True:
        errors.append("abovePit must be true")
    if report.get("floorDots") is not False:
        errors.append("floorDots must be false")
    if report.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("pitDimensions must be 3x3x10")
    summary = report.get("summary", {})
    if summary.get("estimatedTotalEndpointPayloadBytes", 0) <= 0:
        errors.append("estimatedTotalEndpointPayloadBytes must be positive")
    if summary.get("classification") not in {"PATCH", "WATCH", "MAX", "CONFLICT"}:
        errors.append("classification must be known")
    if summary.get("classification") == "CONFLICT":
        errors.append("3x3 endpoint report should not be CONFLICT")
    orientations = report.get("orientations", [])
    if len(orientations) != 24:
        errors.append("orientations table must contain 24 entries")
    for item in orientations:
        cells = item.get("placedCells", [])
        if len(cells) != 4:
            errors.append(f"orientation {item.get('orientationId')} must place four cells")
        for x, y, z in cells:
            if not (0 <= x <= 2 and 0 <= y <= 2 and 0 <= z <= 2):
                errors.append(f"orientation {item.get('orientationId')} cell {x,y,z} is outside expected 3x3 active footprint")
        if item.get("projectedLineSegmentCount", 0) <= 0:
            errors.append(f"orientation {item.get('orientationId')} must contain projected lines")
    if len(report.get("transitions", {})) != 24:
        errors.append("transitions must contain 24 rows")

if not CONFLICT.exists():
    errors.append(f"Missing previous conflict report: {CONFLICT}")

if errors:
    print("ERROR: P04_L true-axis 3x3 pit endpoint payload report verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P04_L true-axis 3x3 pit endpoint payload report verified.")
