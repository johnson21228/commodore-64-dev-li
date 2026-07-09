#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT_PATH = LAB / "dist" / "pieces" / "P02_DOMINO.payload_report.json"
MANIFEST_PATH = LAB / "dist" / "pieces_manifest.json"

errors: list[str] = []

if not REPORT_PATH.exists():
    errors.append(f"Missing report: {REPORT_PATH}")
if not MANIFEST_PATH.exists():
    errors.append(f"Missing manifest: {MANIFEST_PATH}")

if not errors:
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if report.get("schemaVersion") != 1:
        errors.append("report schemaVersion must be 1")
    if report.get("pieceId") != "P02_DOMINO":
        errors.append("report pieceId must be P02_DOMINO")

    scope = report.get("scope", {})
    if scope.get("includedRotations") != ["x_axis", "y_axis"]:
        errors.append("included rotations must be exactly x_axis and y_axis")
    if scope.get("zAxisIncluded") is not False:
        errors.append("z_axis must not be included in the first report")
    if scope.get("runtimeDrawingIncluded") is not False:
        errors.append("runtime drawing must not be included")
    if scope.get("binaryPayloadIncluded") is not False:
        errors.append("binary payload must not be included")

    poses = report.get("poses", [])
    if len(poses) != 400:
        errors.append(f"expected 400 poses, got {len(poses)}")

    by_rotation: dict[str, int] = {}
    pose_ids: set[str] = set()
    for pose in poses:
        rid = pose.get("rotationId")
        by_rotation[rid] = by_rotation.get(rid, 0) + 1
        pose_id = pose.get("poseId")
        if pose_id in pose_ids:
            errors.append(f"duplicate poseId: {pose_id}")
        pose_ids.add(pose_id)

        cells = pose.get("occupiedCells", [])
        if len(cells) != 2:
            errors.append(f"{pose_id} must have exactly 2 occupied cells")

        for cell in cells:
            if not (0 <= cell[0] < 5 and 0 <= cell[1] < 5 and 0 <= cell[2] < 10):
                errors.append(f"{pose_id} occupied cell out of pit bounds: {cell}")

        if pose.get("bitmapByteMaskRecordCount", 0) <= 0:
            errors.append(f"{pose_id} has no bitmap byte/mask records")
        if pose.get("dirtyBitmapOffsetCount") != pose.get("bitmapByteMaskRecordCount"):
            errors.append(f"{pose_id} dirty bitmap count must equal bitmap record count in this report")
        if pose.get("estimatedPayloadBytes", 0) <= 0:
            errors.append(f"{pose_id} estimated payload bytes must be positive")

    if by_rotation.get("x_axis") != 200:
        errors.append(f"x_axis pose count must be 200, got {by_rotation.get('x_axis')}")
    if by_rotation.get("y_axis") != 200:
        errors.append(f"y_axis pose count must be 200, got {by_rotation.get('y_axis')}")
    if "z_axis" in by_rotation:
        errors.append("z_axis must not appear in poses")

    summary = report.get("summary", {})
    if summary.get("poseCount") != 400:
        errors.append("summary poseCount must be 400")
    if summary.get("estimatedTotalPayloadBytes", 0) <= 0:
        errors.append("estimatedTotalPayloadBytes must be positive")
    if summary.get("decisionClassification") not in {"PATCH", "WATCH", "WAIT", "CONFLICT"}:
        errors.append("decisionClassification must be PATCH, WATCH, WAIT, or CONFLICT")

    pieces = manifest.get("pieces", [])
    if len(pieces) != 1:
        errors.append("manifest must contain exactly one piece")
    else:
        piece = pieces[0]
        if piece.get("pieceId") != "P02_DOMINO":
            errors.append("manifest pieceId must be P02_DOMINO")
        if piece.get("poseCount") != 400:
            errors.append("manifest poseCount must be 400")
        if piece.get("binaryPayload") is not None:
            errors.append("manifest binaryPayload must be null for report-only stage")
        if piece.get("estimatedTotalPayloadBytes") != summary.get("estimatedTotalPayloadBytes"):
            errors.append("manifest estimatedTotalPayloadBytes must match report summary")

if errors:
    print("ERROR: P02_DOMINO payload report verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P02_DOMINO payload report verified (400 poses, x/y rotations only, report-only stage).")
