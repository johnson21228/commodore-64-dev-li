#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"

errors: list[str] = []

if not REPORT.exists():
    errors.append(f"Missing report: {REPORT}")
else:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("pieceId") != "P03_ELBOW":
        errors.append("report must be for P03_ELBOW")
    if report.get("reportType") != "true-axis endpoint 3x3 green-line pit payload report":
        errors.append("wrong reportType")
    if report.get("axisControls") != {"A":"+x","Q":"-x","S":"+y","W":"-y","D":"+z","E":"-z"}:
        errors.append("axis controls must be true x/y/z controls")
    if report.get("abovePit") is not True:
        errors.append("abovePit must be true")
    if report.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("pitDimensions must be 3x3x10")
    if report.get("floorLines") is not False:
        errors.append("floorLines must be false")
    orientation_count = report.get("orientationCount", 0)
    if orientation_count < 8:
        errors.append("P03_ELBOW true-axis report should have multiple orientations")
    summary = report.get("summary", {})
    if summary.get("classification") == "CONFLICT":
        errors.append("P03_ELBOW endpoint payload should not be CONFLICT")
    if summary.get("estimatedTotalEndpointPayloadBytes", 0) <= 0:
        errors.append("estimatedTotalEndpointPayloadBytes must be positive")
    orientations = report.get("orientations", [])
    if len(orientations) != orientation_count:
        errors.append("orientations table must match orientationCount")
    for item in orientations:
        cells = item.get("placedCells", [])
        if len(cells) != 3:
            errors.append(f"orientation {item.get('orientationId')} must place three cells")
        for x, y, z in cells:
            if not (0 <= x <= 2 and 0 <= y <= 2 and 0 <= z <= 2):
                errors.append(f"orientation {item.get('orientationId')} cell {x,y,z} outside expected 3x3 active footprint")
    transitions = report.get("transitions", {})
    if len(transitions) != orientation_count:
        errors.append("transitions must match orientationCount")
    for row in transitions.values():
        if set(row.keys()) != {"A", "Q", "S", "W", "D", "E"}:
            errors.append("each transition row must include all six controls")
            break

if errors:
    print("ERROR: P03_ELBOW true-axis endpoint 3x3 green-line pit payload report verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW true-axis endpoint 3x3 green-line pit payload report verified.")
