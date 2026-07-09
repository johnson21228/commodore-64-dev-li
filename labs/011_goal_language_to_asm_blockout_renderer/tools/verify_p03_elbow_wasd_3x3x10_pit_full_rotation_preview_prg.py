#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"
META = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_full_rotation_preview_metadata.json"
PRG = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_full_rotation_preview.prg"

errors: list[str] = []

if not REPORT.exists():
    errors.append(f"missing report: {REPORT}")
if not META.exists():
    errors.append(f"missing metadata: {META}")
if not PRG.exists():
    errors.append(f"missing PRG: {PRG}")

if not errors:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    meta = json.loads(META.read_text(encoding="utf-8"))
    prg_size = PRG.stat().st_size

    if meta.get("pieceId") != "P03_ELBOW":
        errors.append("preview must be for P03_ELBOW")
    if meta.get("mode") != "P03_ELBOW WASD 3x3x10 pit full-rotation preview":
        errors.append("unexpected preview mode")
    if meta.get("orientationCount") != 12:
        errors.append("P03_ELBOW must have 12 orientations")
    if meta.get("runtimeLineDrawing") is not True:
        errors.append("preview should use runtime endpoint line drawing")

    if report.get("projectionContract") != "WASD_3x3x10":
        errors.append("source report projectionContract must be WASD_3x3x10")

    anchor = report.get("anchor")
    anchor_text = anchor if isinstance(anchor, str) else json.dumps(anchor, sort_keys=True)
    if "center" not in anchor_text.lower() and "current" not in anchor_text.lower() and "3x3" not in anchor_text.lower():
        errors.append(f"source report anchor should describe centered/current 3x3 placement, got {anchor!r}")

    sizes = meta.get("sizes", {})
    if sizes.get("pitRecordBytes") != 1992:
        errors.append("dotted pit should be 1992 bytes")
    if sizes.get("payloadBytes", 0) < 12000:
        errors.append("arrow translation preview should use orientation+cursor pose payloads")
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("programUsedBytes must fit in available PRG image")
    if prg_size != meta.get("prgBytes"):
        errors.append("metadata prgBytes must match actual PRG size")

    report_translation = report.get("translationControls", {})
    meta_translation = meta.get("inputTranslation") or meta.get("translationControls") or {}
    if not report_translation and not meta_translation:
        errors.append("report or metadata should record cursor-arrow translation controls")

    pose_payloads = report.get("posePayloads") or report.get("poses") or []
    if isinstance(pose_payloads, list) and len(pose_payloads) != 108:
        errors.append("preview source report should include 108 orientation+cursor pose payloads")

if errors:
    print("ERROR: P03_ELBOW WASD 3x3x10 pit full-rotation preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW WASD 3x3x10 pit full-rotation preview verified.")
