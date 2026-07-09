#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
svg_path = ROOT / "captures" / "blockout_gameboard_projection.svg"

if not svg_path.exists():
    raise SystemExit("Missing captures/blockout_gameboard_projection.svg")

text = svg_path.read_text(encoding="utf-8")
for required in [
    "<svg",
    "Lab 011 gameboard projection",
    "5x5x12 pit",
    'class="top"',
    'class="side"',
    'class="depth"',
]:
    if required not in text:
        raise SystemExit(f"SVG projection missing required marker: {required}")

if text.count("<line ") < 20:
    raise SystemExit("SVG projection has too few line segments to represent the pit")

print("OK: gameboard projection SVG verified.")
