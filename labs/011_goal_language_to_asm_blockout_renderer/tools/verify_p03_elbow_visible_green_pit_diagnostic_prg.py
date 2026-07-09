#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p03_elbow_visible_green_pit_diagnostic.prg"
META = LAB / "dist" / "p03_elbow_visible_green_pit_diagnostic_metadata.json"
BUILDER = LAB / "tools" / "build_p03_elbow_visible_green_pit_diagnostic_prg.py"

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
    if meta.get("mode") != "P03_ELBOW visible green 3x3x10 pit diagnostic":
        errors.append("wrong mode")
    if meta.get("pitOnly") is not True:
        errors.append("pitOnly must be true")
    if meta.get("activeBlockDrawn") is not False:
        errors.append("activeBlockDrawn must be false")
    if meta.get("runtimeLineDrawing") is not False:
        errors.append("runtimeLineDrawing must be false")
    if "VISIBLE diagnostic" not in meta.get("pitStyle", ""):
        errors.append("pitStyle must identify visible diagnostic")
    if 'jsr("draw_endpoint_lines")' in builder_text.split('a.label("draw_frame")', 1)[1].split('a.label("load_orientation_payload")', 1)[0]:
        errors.append("draw_frame must not call draw_endpoint_lines")
    sizes = meta.get("sizes", {})
    if sizes.get("pitRecordBytes", 0) <= 1000:
        errors.append("visible pit should have substantial pit records")
    if sizes.get("programUsedBytes", 999999) >= sizes.get("availablePrgImageBytes", 0):
        errors.append("program must fit")

if errors:
    print("ERROR: visible green pit diagnostic verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: visible green 3x3x10 pit diagnostic PRG verified.")
