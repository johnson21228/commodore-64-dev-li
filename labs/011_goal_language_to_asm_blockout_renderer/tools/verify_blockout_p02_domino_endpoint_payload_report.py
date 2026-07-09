#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT_PATH = LAB / "dist" / "pieces" / "P02_DOMINO.endpoint_payload_report.json"
RAW_REPORT_PATH = LAB / "dist" / "pieces" / "P02_DOMINO.payload_report.json"
MANIFEST_PATH = LAB / "dist" / "pieces_manifest.json"

errors: list[str] = []

for path in [REPORT_PATH, RAW_REPORT_PATH, MANIFEST_PATH]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    raw = json.loads(RAW_REPORT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    if report.get("schemaVersion") != 1:
        errors.append("endpoint report schemaVersion must be 1")
    if report.get("pieceId") != "P02_DOMINO":
        errors.append("endpoint report pieceId must be P02_DOMINO")
    if report.get("reportType") != "blockout_piece_endpoint_payload_report":
        errors.append("endpoint reportType mismatch")

    scope = report.get("scope", {})
    if scope.get("includedRotations") != ["x_axis", "y_axis"]:
        errors.append("included rotations must be exactly x_axis and y_axis")
    if scope.get("zAxisIncluded") is not False:
        errors.append("z_axis must not be included")
    if scope.get("runtimeDrawingIncluded") is not False:
        errors.append("runtime drawing must not be included")
    if scope.get("binaryPayloadIncluded") is not False:
        errors.append("binary payload must not be included")

    poses = report.get("poses", [])
    if len(poses) != 400:
        errors.append(f"expected 400 endpoint poses, got {len(poses)}")

    by_rotation: dict[str, int] = {}
    for pose in poses:
        rid = pose.get("rotationId")
        by_rotation[rid] = by_rotation.get(rid, 0) + 1
        if pose.get("projectedLineSegmentCount", 0) <= 0:
            errors.append(f"{pose.get('poseId')} must have projected line segments")
        if pose.get("estimatedEndpointPayloadBytes", 0) <= 0:
            errors.append(f"{pose.get('poseId')} endpoint bytes must be positive")
        if pose.get("estimatedGridReferencePayloadBytes", 0) <= 0:
            errors.append(f"{pose.get('poseId')} grid-reference bytes must be positive")
        box = pose.get("dirtyBoundingBox", {})
        for key in ["minX", "minY", "maxX", "maxY"]:
            if key not in box:
                errors.append(f"{pose.get('poseId')} missing dirty bbox key {key}")

    if by_rotation.get("x_axis") != 200:
        errors.append(f"x_axis pose count must be 200, got {by_rotation.get('x_axis')}")
    if by_rotation.get("y_axis") != 200:
        errors.append(f"y_axis pose count must be 200, got {by_rotation.get('y_axis')}")
    if "z_axis" in by_rotation:
        errors.append("z_axis must not appear in endpoint poses")

    summary = report.get("summary", {})
    raw_bytes = raw.get("summary", {}).get("estimatedTotalPayloadBytes")
    endpoint_bytes = summary.get("estimatedEndpointPayloadBytes")
    grid_bytes = summary.get("estimatedGridReferencePayloadBytes")

    if summary.get("poseCount") != 400:
        errors.append("summary poseCount must be 400")
    if endpoint_bytes is None or endpoint_bytes <= 0:
        errors.append("estimatedEndpointPayloadBytes must be positive")
    if grid_bytes is None or grid_bytes <= 0:
        errors.append("estimatedGridReferencePayloadBytes must be positive")
    if raw_bytes is None or raw_bytes <= 0:
        errors.append("raw byte/mask bytes must be positive")
    else:
        if endpoint_bytes is not None and endpoint_bytes >= raw_bytes:
            errors.append("endpoint estimate must be smaller than raw byte/mask estimate")
        if grid_bytes is not None and grid_bytes >= raw_bytes:
            errors.append("grid-reference estimate must be smaller than raw byte/mask estimate")

    if summary.get("endpointDecisionClassification") not in {"PATCH", "WATCH", "WAIT", "CONFLICT"}:
        errors.append("endpointDecisionClassification invalid")
    if summary.get("gridReferenceDecisionClassification") not in {"PATCH", "WATCH", "WAIT", "CONFLICT"}:
        errors.append("gridReferenceDecisionClassification invalid")

    pieces = manifest.get("pieces", [])
    p02 = [p for p in pieces if p.get("pieceId") == "P02_DOMINO"]
    if len(p02) != 1:
        errors.append("manifest must contain exactly one P02_DOMINO entry")
    else:
        entry = p02[0]
        if entry.get("endpointPayloadReport") != "pieces/P02_DOMINO.endpoint_payload_report.json":
            errors.append("manifest must reference endpoint report")
        if entry.get("binaryPayload") is not None:
            errors.append("binaryPayload must remain null")
        if entry.get("estimatedEndpointPayloadBytes") != endpoint_bytes:
            errors.append("manifest endpoint bytes must match report")

if errors:
    print("ERROR: P02_DOMINO endpoint payload report verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P02_DOMINO endpoint/topology payload report verified.")
