#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PRG = LAB / "dist" / "p02_domino_white_dashed_pit_preview.prg"
META = LAB / "dist" / "p02_domino_white_dashed_pit_preview_metadata.json"
BASE_PRG = LAB / "dist" / "p02_domino_top_endpoint_preview.prg"

errors: list[str] = []

for path in [PRG, META, BASE_PRG]:
    if not path.exists():
        errors.append(f"Missing required file: {path}")

if not errors:
    data = PRG.read_bytes()
    meta = json.loads(META.read_text(encoding="utf-8"))

    if data[:2] != bytes([0x01, 0x08]):
        errors.append("PRG must load at $0801")

    selected = meta.get("selectedPose", {})
    if selected.get("pieceId") != "P02_DOMINO":
        errors.append("selected piece must be P02_DOMINO")
    if selected.get("rotationId") != "x_axis":
        errors.append("selected rotation must be x_axis")
    if selected.get("z") != 0:
        errors.append("selected pose must be top level z=0")

    line_language = meta.get("lineLanguage", {})
    if "dashed" not in line_language.get("pit", ""):
        errors.append("pit line language must be dashed")
    if "solid" not in line_language.get("activeBlock", ""):
        errors.append("active block line language must be solid")

    colors = meta.get("colors", {})
    if colors.get("pitColor") != "white" or colors.get("activeBlockColor") != "white":
        errors.append("pit and active block must both be white for this preview")

    if meta.get("runtimeLineDrawing") is not False:
        errors.append("preview must not claim runtime line drawing")
    if meta.get("previewOnly") is not True:
        errors.append("previewOnly must be true")

    if meta.get("pitTouchedCells", 0) <= 0:
        errors.append("pit must touch cells")
    if meta.get("blockTouchedCells", 0) <= 0:
        errors.append("block must touch cells")

if errors:
    print("ERROR: white dashed pit preview verification failed.")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("OK: P02_DOMINO white dashed pit preview PRG verified.")
