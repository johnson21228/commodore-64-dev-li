#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = [
    ROOT / "captures" / "blockout_single_cube_polygon_preview.svg",
    ROOT / "captures" / "blockout_single_cube_red_shaded_faces.svg",
    ROOT / "captures" / "blockout_pit_with_red_cube.svg",
    ROOT / "dist" / "single_cube_polygon_faces.json",
]

for path in paths:
    if not path.exists():
        raise SystemExit(f"Missing single-cube artifact: {path.relative_to(ROOT)}")

svg = (ROOT / "captures" / "blockout_pit_with_red_cube.svg").read_text(encoding="utf-8")
for required in [
    "<polygon",
    "pit_top",
    "pit_depth",
    "top_face",
    "north_wall",
    "east_wall",
    "south_wall",
    "west_wall",
    "off-side cube in perspective pit",
    "red_light",
    "red_mid",
    "red_mid_dark",
    "red_dark",
    "red_deep",
]:
    if required not in svg:
        raise SystemExit(f"Pit-context red cube SVG missing marker: {required}")

data = json.loads((ROOT / "dist" / "single_cube_polygon_faces.json").read_text(encoding="utf-8"))
if data.get("projection") != "top_down_perspective_rings":
    raise SystemExit("Single-cube polygon proof is not using top_down_perspective_rings")

cube = data.get("cube", {})
if cube.get("palette") != "solid_red_shaded":
    raise SystemExit("Single-cube proof does not declare solid_red_shaded palette")
if cube.get("positioning") != "off_side_left_visible_faces":
    raise SystemExit("Single-cube proof is not off-side with visible faces")
if cube.get("x") != 0 or cube.get("height") != 2:
    raise SystemExit(f"Unexpected cube position/height for side-face proof: {cube}")

faces = data.get("faces", [])
if len(faces) != 5:
    raise SystemExit(f"Expected 5 cube faces, found {len(faces)}")

for face in faces:
    pts = face.get("points", [])
    if len(pts) != 4:
        raise SystemExit(f"Face is not a quad: {face}")
    for p in pts:
        if not 0 <= p["x"] <= 255 or not 0 <= p["y"] <= 199:
            raise SystemExit(f"Face coordinate out of C64 bounds: {face}")

print("OK: off-side red cube in perspective pit verified.")
