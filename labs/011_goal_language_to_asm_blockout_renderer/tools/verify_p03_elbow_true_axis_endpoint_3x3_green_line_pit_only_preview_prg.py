#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p03_elbow_true_axis_endpoint_3x3_green_line_pit_only_preview.prg"
META = LAB / "dist" / "p03_elbow_true_axis_endpoint_3x3_green_line_pit_only_preview_metadata.json"
BUILDER = LAB / "tools" / "build_p03_elbow_true_axis_endpoint_3x3_green_line_pit_only_preview_prg.py"

errors: list[str] = []

for path in [PRG, META, BUILDER]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))
    builder_text = BUILDER.read_text(encoding="utf-8")

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")
    if len(data) != 30719:
        errors.append("PRG image should be fixed lab image size 30719 bytes")
    if meta.get("pieceId") != "P03_ELBOW":
        errors.append("preview must be for P03_ELBOW")
    if meta.get("mode") != "P03_ELBOW 3x3 green-line pit-only diagnostic preview":
        errors.append("wrong preview mode")
    if meta.get("pitOnly") is not True:
        errors.append("pitOnly must be true")
    if meta.get("activeBlockDrawn") is not False:
        errors.append("activeBlockDrawn must be false")
    if meta.get("runtimeLineDrawing") is not False:
        errors.append("runtimeLineDrawing must be false for pit-only diagnostic")
    if meta.get("pitDimensions") != {"widthCells": 3, "heightCells": 3, "depthCells": 10}:
        errors.append("pitDimensions must be 3x3x10")
    if meta.get("floorLines") is not False:
        errors.append("floorLines must be false")
    if "green" not in meta.get("pitStyle", "") or "grid lines" not in meta.get("pitStyle", ""):
        errors.append("pitStyle must describe green grid lines")
    draw_frame_body = builder_text.split('a.label("draw_frame")', 1)[1].split('a.label("load_orientation_payload")', 1)[0]
    if 'jsr("draw_endpoint_lines")' in draw_frame_body:
        errors.append("draw_frame must not call draw_endpoint_lines")
    sizes = meta.get("sizes", {})
    if sizes.get("pitRecordBytes", 0) <= 1000:
        errors.append("pitRecordBytes should show substantial green line pit")
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("program must fit within available PRG image bytes")

if errors:
    print("ERROR: P03_ELBOW green-line pit-only diagnostic verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P03_ELBOW green-line pit-only diagnostic PRG verified.")
