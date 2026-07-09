#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
intent = json.loads((ROOT / "goal" / "renderer_intent.json").read_text(encoding="utf-8"))
entries = json.loads((ROOT / "dist" / "projection_table.json").read_text(encoding="utf-8"))
segments = json.loads((ROOT / "dist" / "pit_line_segments.json").read_text(encoding="utf-8"))

pit = intent["pit"]
expected = pit["width"] * pit["depth"] * pit["height"]
if len(entries) != expected:
    raise SystemExit(f"Expected {expected} projection entries; found {len(entries)}")

for e in entries:
    if not 0 <= e["screen_x"] <= 255:
        raise SystemExit(f"screen_x out of byte range: {e}")
    if not 0 <= e["screen_y"] <= 199:
        raise SystemExit(f"screen_y out of C64 screen range: {e}")

if not segments:
    raise SystemExit("No pit line segments generated")

for s in segments:
    for key in ["x1", "y1", "x2", "y2"]:
        if not 0 <= s[key] <= 255:
            raise SystemExit(f"segment coordinate out of byte range: {s}")

print("OK: projection table and pit line segment geometry verified.")
