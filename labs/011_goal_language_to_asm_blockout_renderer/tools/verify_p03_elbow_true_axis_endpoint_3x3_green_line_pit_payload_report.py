#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"

errors: list[str] = []

def infer_pit_dimensions(report: dict) -> tuple[int | None, int | None, int | None]:
    pit = report.get("pitDimensions")
    if isinstance(pit, dict):
        width = pit.get("width", pit.get("w", pit.get("PIT_W")))
        height = pit.get("height", pit.get("h", pit.get("PIT_H")))
        depth = pit.get("visualDepth", pit.get("depth", pit.get("PIT_VISUAL_DEPTH")))
        if width is not None or height is not None or depth is not None:
            return int(width or -1), int(height or -1), int(depth or -1)

    contract = report.get("projectionContract", "")
    if contract == "WASD_3x3x10":
        return 3, 3, 10

    xs: list[int] = []
    ys: list[int] = []
    zs: list[int] = []
    for item in report.get("orientations", []):
        for cell in item.get("placedCells", []):
            if len(cell) == 3:
                x, y, z = [int(v) for v in cell]
                xs.append(x); ys.append(y); zs.append(z)
    if xs and ys and zs:
        return max(xs) + 1, max(ys) + 1, max(10, max(zs))
    return None, None, None

if not REPORT.exists():
    errors.append(f"missing report: {REPORT}")
else:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    if report.get("pieceId") != "P03_ELBOW":
        errors.append("report must be for P03_ELBOW")
    if report.get("projectionContract") != "WASD_3x3x10":
        errors.append("projectionContract must be WASD_3x3x10")

    anchor = report.get("anchor")
    anchor_text = anchor if isinstance(anchor, str) else json.dumps(anchor, sort_keys=True)
    if "center" not in anchor_text.lower() and "current" not in anchor_text.lower() and "3x3" not in anchor_text.lower():
        errors.append(f"anchor should describe centered/current 3x3 placement, got {anchor!r}")

    if report.get("orientationCount") != 12:
        errors.append("P03_ELBOW report must have 12 orientations")

    summary = report.get("summary", {})
    if summary.get("classification") == "CONFLICT":
        errors.append("P03_ELBOW endpoint payload should not be CONFLICT")
    expected_max = summary.get("maxProjectedLineSegmentsPerPose", summary.get("maxProjectedLineSegmentsPerOrientation"))
    if expected_max != 28:
        errors.append("each P03_ELBOW pose should have 28 projected line segments")

    width, height, depth = infer_pit_dimensions(report)
    if (width, height, depth) != (3, 3, 10):
        errors.append(f"pit contract must resolve to 3x3x10, got width={width!r} height={height!r} depth={depth!r}")

    orientations = report.get("orientations", [])
    if len(orientations) != 12:
        errors.append("orientations length must be 12")
    else:
        for item in orientations:
            if item.get("projectedLineSegmentCount") != 28:
                errors.append(f"orientation {item.get('orientationId')} should have 28 segments")
            placed = item.get("placedCells", [])
            for cell in placed:
                if len(cell) != 3:
                    errors.append(f"bad placed cell: {cell!r}")
                    continue
                x, y, z = [int(v) for v in cell]
                if not (0 <= x <= 2 and 0 <= y <= 2 and 0 <= z <= 10):
                    errors.append(f"placed cell outside 3x3x10 pit: {cell!r}")
            for seg in item.get("segments", []):
                for key in ["x1", "y1", "x2", "y2"]:
                    v = int(seg.get(key, -1))
                    if not 0 <= v <= 255:
                        errors.append(f"endpoint out of 8-bit range: {key}={v}")

    pose_payloads = report.get("posePayloads") or report.get("poses") or report.get("posePayloadIndex") or []
    if isinstance(pose_payloads, list) and pose_payloads and len(pose_payloads) != 108:
        errors.append("translation payload should contain 108 pose payloads (12 orientations * 3 x * 3 y)")

    transitions = report.get("transitions", {})
    if sorted(transitions.get("0", {}).keys()) != ["A", "D", "E", "Q", "S", "W"]:
        errors.append("transition keys must be A/Q/S/W/D/E")

    translation = report.get("translationControls", {})
    expected_translation_keys = {"cursorLeft", "cursorRight", "cursorUp", "cursorDown"}
    if translation and set(translation.keys()) != expected_translation_keys:
        errors.append("translationControls must expose cursorLeft/cursorRight/cursorUp/cursorDown")

if errors:
    print("ERROR: P03_ELBOW true-axis endpoint 3x3 green-line pit payload report verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW true-axis endpoint 3x3 green-line pit payload report verified.")
