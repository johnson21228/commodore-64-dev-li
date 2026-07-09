#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CAPTURES = ROOT / "captures"

def ensure_generated() -> None:
    if not (DIST / "pit_line_segments.json").exists():
        subprocess.run(["python3", "tools/generate_blockout_renderer.py"], cwd=ROOT, check=True)

def svg_line(x1: int, y1: int, x2: int, y2: int, klass: str = "grid") -> str:
    return f"<line class={chr(34)}{klass}{chr(34)} x1={chr(34)}{x1}{chr(34)} y1={chr(34)}{y1}{chr(34)} x2={chr(34)}{x2}{chr(34)} y2={chr(34)}{y2}{chr(34)} />"

def main() -> None:
    ensure_generated()

    intent = json.loads((ROOT / "goal" / "renderer_intent.json").read_text(encoding="utf-8"))
    segments = json.loads((DIST / "pit_line_segments.json").read_text(encoding="utf-8"))

    xs = []
    ys = []
    for s in segments:
        xs.extend([s["x1"], s["x2"]])
        ys.extend([s["y1"], s["y2"]])

    min_x = min(xs) - 24
    max_x = max(xs) + 24
    min_y = min(ys) - 24
    max_y = max(ys) + 32
    width = max_x - min_x
    height = max_y - min_y

    def tx(x: int) -> int:
        return x - min_x

    def ty(y: int) -> int:
        return y - min_y

    drawn_lines = []
    for s in segments:
        start = tuple(s["start"])
        end = tuple(s["end"])

        klass = "grid"
        if start[2] == 0 and end[2] == 0:
            klass = "top"
        elif start[2] != end[2]:
            klass = "depth"
        elif start[2] == end[2] and start[2] > 0:
            klass = "side"

        drawn_lines.append(svg_line(tx(s["x1"]), ty(s["y1"]), tx(s["x2"]), ty(s["y2"]), klass))

    projection_type = escape(intent.get("projection", {}).get("type", "unknown"))

    svg_parts = [
        f"<svg xmlns={chr(34)}http://www.w3.org/2000/svg{chr(34)} width={chr(34)}{width}{chr(34)} height={chr(34)}{height}{chr(34)} viewBox={chr(34)}0 0 {width} {height}{chr(34)} role={chr(34)}img{chr(34)} aria-labelledby={chr(34)}title desc{chr(34)}>",
        "  <title id=\"title\">Lab 011 gameboard projection preview</title>",
        "  <desc id=\"desc\">A top-down perspective pit generated from renderer_intent.json through pit_line_segments.json.</desc>",
        "  <style>",
        "    .bg { fill: #11131a; }",
        "    .top { stroke: #f7d85c; stroke-width: 2; vector-effect: non-scaling-stroke; }",
        "    .side { stroke: #66d9ef; stroke-width: 1.3; opacity: 0.78; vector-effect: non-scaling-stroke; }",
        "    .depth { stroke: #ff7a7a; stroke-width: 1.8; opacity: 0.92; vector-effect: non-scaling-stroke; }",
        "    .grid { stroke: #9aa0a6; stroke-width: 1; opacity: 0.55; vector-effect: non-scaling-stroke; }",
        "    .label { fill: #e8eaed; font: 10px monospace; }",
        "    .small { fill: #b8bec8; font: 8px monospace; }",
        "  </style>",
        f"  <rect class=\"bg\" x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\" />",
        *["  " + line for line in drawn_lines],
        "  <text class=\"label\" x=\"8\" y=\"14\">Lab 011 top-down perspective pit</text>",
        f"  <text class=\"small\" x=\"8\" y=\"28\">5x5x12 pit · {projection_type} · generated from governed line segments</text>",
        "</svg>",
        "",
    ]

    CAPTURES.mkdir(parents=True, exist_ok=True)
    out = CAPTURES / "blockout_gameboard_projection.svg"
    out.write_text(chr(10).join(svg_parts), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
