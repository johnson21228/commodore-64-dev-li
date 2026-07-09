#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
intent = json.loads((ROOT / "goal" / "renderer_intent.json").read_text(encoding="utf-8"))
metadata_path = ROOT / "dist" / "projection_metadata.json"

if intent["projection"].get("type") != "top_down_perspective_rings":
    raise SystemExit("Projection is not top_down_perspective_rings")

rings = intent["projection"].get("depth_rings", [])
if len(rings) < 3:
    raise SystemExit("Expected at least three explicit perspective depth rings")

last_z = -1
last_w = 10**9
last_h = 10**9
for ring in rings:
    z = ring["z"]
    w = ring["width"]
    h = ring["height"]
    if z <= last_z:
        raise SystemExit(f"Depth rings must be strictly increasing by z: {rings}")
    if w >= last_w or h >= last_h:
        raise SystemExit(f"Perspective rings must shrink with depth: {rings}")
    if not 0 <= w <= 255 or not 0 <= h <= 199:
        raise SystemExit(f"Ring dimensions out of C64-visible bounds: {ring}")
    last_z, last_w, last_h = z, w, h

if not metadata_path.exists():
    raise SystemExit("Missing dist/projection_metadata.json")

metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
if metadata.get("projection_type") != "top_down_perspective_rings":
    raise SystemExit("Projection metadata does not record top_down_perspective_rings")

print("OK: explicit top-down perspective ring projection verified.")
