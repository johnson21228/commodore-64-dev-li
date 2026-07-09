#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"
META = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_solid_active_preview_metadata.json"
PRG = LAB / "dist" / "p03_elbow_wasd_3x3x10_pit_solid_active_preview.prg"

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

    if meta.get("pieceId") != "P03_ELBOW":
        errors.append("solid preview must be for P03_ELBOW")
    if meta.get("mode") != "P03_ELBOW WASD 3x3x10 pit solid-active preview":
        errors.append("unexpected solid preview mode")
    if meta.get("orientationCount") != 12:
        errors.append("P03_ELBOW must have 12 orientations")
    if meta.get("runtimeLineDrawing") is not False:
        errors.append("solid-active preview should not use runtime line drawing for the active piece")
    if meta.get("activeSolidBoxes") is not True:
        errors.append("solid-active preview must declare activeSolidBoxes")
    if meta.get("activeBoxPayloadBytes", 0) < 1000:
        errors.append("active box payload should be present for all orientation+cursor poses")
    if report.get("projectionContract") != "WASD_3x3x10":
        errors.append("source report projectionContract must be WASD_3x3x10")
    pose_payloads = report.get("posePayloads") or []
    if len(pose_payloads) != 108:
        errors.append("source report should include 108 orientation+cursor pose payloads")
    if any("placedCells" not in p for p in pose_payloads):
        errors.append("solid-active preview requires placedCells in every pose")
    sizes = meta.get("sizes", {})
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("programUsedBytes must fit in available PRG image")
    if PRG.stat().st_size != meta.get("prgBytes"):
        errors.append("metadata prgBytes must match actual PRG size")

if errors:
    print("ERROR: P03_ELBOW WASD 3x3x10 solid-active preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW WASD 3x3x10 pit solid-active preview verified.")
