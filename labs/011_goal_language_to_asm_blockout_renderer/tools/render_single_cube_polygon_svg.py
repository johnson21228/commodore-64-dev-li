#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CAPTURES = ROOT / "captures"

def ensure_generated() -> None:
    if not (DIST / "projection_metadata.json").exists():
        subprocess.run(["python3", "tools/generate_blockout_renderer.py"], cwd=ROOT, check=True)

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def ring_for_z(intent: dict, z: int) -> dict:
    rings = sorted(intent["projection"]["depth_rings"], key=lambda r: r["z"])
    if z <= rings[0]["z"]:
        return dict(rings[0])
    if z >= rings[-1]["z"]:
        return dict(rings[-1])
    for a, b in zip(rings, rings[1:]):
        if a["z"] <= z <= b["z"]:
            span = b["z"] - a["z"]
            t = 0 if span == 0 else (z - a["z"]) / span
            return {
                "z": z,
                "width": round(lerp(a["width"], b["width"], t)),
                "height": round(lerp(a["height"], b["height"], t)),
            }
    raise ValueError(f"No ring for z={z}")

def project(intent: dict, x: int, y: int, z: int) -> tuple[int, int]:
    p = intent["projection"]
    pit = intent["pit"]
    ring = ring_for_z(intent, z)
    left = p["center_x"] - ring["width"] / 2
    top = p["center_y"] - ring["height"] / 2
    sx = round(left + x * ring["width"] / pit["width"])
    sy = round(top + y * ring["height"] / pit["depth"])
    return sx, sy

def face(points: list[tuple[int, int]], name: str, shade: str) -> dict:
    return {
        "name": name,
        "shade": shade,
        "points": [{"x": x, "y": y} for x, y in points],
    }

def svg_poly(points: list[dict], klass: str) -> str:
    pts = " ".join(f"{p['x']},{p['y']}" for p in points)
    return f'<polygon class="{klass}" points="{pts}" />'

def svg_line(x1: int, y1: int, x2: int, y2: int, klass: str) -> str:
    return f'<line class="{klass}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'

def cube_faces(intent: dict) -> tuple[dict, list[dict]]:
    # Off-side cube proof: placed left/front-ish in the pit and given 2 z-units
    # so the side faces are visible in the perspective preview and C64 proof.
    cube = {
        "x": 0,
        "y": 1,
        "z": 3,
        "width": 1,
        "depth": 1,
        "height": 2,
        "palette": "solid_red_shaded",
        "positioning": "off_side_left_visible_faces",
    }

    x0, y0, z0 = cube["x"], cube["y"], cube["z"]
    x1, y1, z1 = x0 + cube["width"], y0 + cube["depth"], z0 + cube["height"]

    a = project(intent, x0, y0, z0)
    b = project(intent, x1, y0, z0)
    c = project(intent, x1, y1, z0)
    d = project(intent, x0, y1, z0)

    e = project(intent, x0, y0, z1)
    f = project(intent, x1, y0, z1)
    g = project(intent, x1, y1, z1)
    h = project(intent, x0, y1, z1)

    faces = [
        face([e, f, b, a], "north_wall", "red_dark"),
        face([f, g, c, b], "east_wall", "red_mid"),
        face([g, h, d, c], "south_wall", "red_deep"),
        face([h, e, a, d], "west_wall", "red_mid_dark"),
        face([a, b, c, d], "top_face", "red_light"),
    ]
    return cube, faces

def class_for_segment(segment: dict) -> str:
    start = tuple(segment["start"])
    end = tuple(segment["end"])
    if start[2] == 0 and end[2] == 0:
        return "pit_top"
    if start[2] != end[2]:
        return "pit_depth"
    if start[2] == end[2] and start[2] > 0:
        return "pit_side"
    return "pit_grid"

def shifted_points(points: list[dict], min_x: int, min_y: int) -> list[dict]:
    return [{"x": p["x"] - min_x, "y": p["y"] - min_y} for p in points]

def write_cube_only_svg(faces: list[dict]) -> None:
    xs = [p["x"] for f in faces for p in f["points"]]
    ys = [p["y"] for f in faces for p in f["points"]]
    min_x, max_x = min(xs) - 28, max(xs) + 28
    min_y, max_y = min(ys) - 28, max(ys) + 32
    width, height = max_x - min_x, max_y - min_y

    polygons = []
    for fdata in faces:
        pts = shifted_points(fdata["points"], min_x, min_y)
        polygons.append(svg_poly(pts, f"cube {fdata['name']} {fdata['shade']}"))

    svg_parts = svg_document(
        width,
        height,
        polygons,
        "Lab 011 off-side solid red cube proof",
        "off-side cube · solid red shaded faces",
    )

    svg_text = "\n".join(svg_parts)
    (CAPTURES / "blockout_single_cube_polygon_preview.svg").write_text(svg_text, encoding="utf-8")
    (CAPTURES / "blockout_single_cube_red_shaded_faces.svg").write_text(svg_text, encoding="utf-8")

def svg_document(width: int, height: int, body: list[str], title: str, label: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">{title}</title>',
        '  <desc id="desc">A top-down perspective pit with a solid red shaded cube face proof.</desc>',
        '  <style>',
        '    .bg { fill: #11131a; }',
        '    .pit_top { stroke: #f7d85c; stroke-width: 1.6; opacity: 0.85; vector-effect: non-scaling-stroke; }',
        '    .pit_side { stroke: #66d9ef; stroke-width: 1.1; opacity: 0.55; vector-effect: non-scaling-stroke; }',
        '    .pit_depth { stroke: #ff7a7a; stroke-width: 1.2; opacity: 0.75; vector-effect: non-scaling-stroke; }',
        '    .pit_grid { stroke: #9aa0a6; stroke-width: 1; opacity: 0.45; vector-effect: non-scaling-stroke; }',
        '    .cube { stroke: #ffcccc; stroke-width: 1.2; vector-effect: non-scaling-stroke; }',
        '    .red_light { fill: #ff4a3d; }',
        '    .red_mid { fill: #d92f2b; }',
        '    .red_mid_dark { fill: #b32124; }',
        '    .red_dark { fill: #8f171d; }',
        '    .red_deep { fill: #661016; }',
        '    .label { fill: #ffe3e3; font: 10px monospace; }',
        '    .small { fill: #b8bec8; font: 8px monospace; }',
        '  </style>',
        f'  <rect class="bg" x="0" y="0" width="{width}" height="{height}" />',
        *["  " + item for item in body],
        f'  <text class="label" x="8" y="14">{label}</text>',
        '  <text class="small" x="8" y="28">cube is off-center in the governed perspective pit</text>',
        '</svg>',
        '',
    ]

def write_pit_with_cube_svg(faces: list[dict], segments: list[dict]) -> None:
    xs = []
    ys = []
    for s in segments:
        xs.extend([s["x1"], s["x2"]])
        ys.extend([s["y1"], s["y2"]])
    for f in faces:
        for p in f["points"]:
            xs.append(p["x"])
            ys.append(p["y"])

    min_x, max_x = min(xs) - 24, max(xs) + 24
    min_y, max_y = min(ys) - 24, max(ys) + 34
    width, height = max_x - min_x, max_y - min_y

    body: list[str] = []

    # Pit context first.
    for s in segments:
        body.append(svg_line(
            s["x1"] - min_x,
            s["y1"] - min_y,
            s["x2"] - min_x,
            s["y2"] - min_y,
            class_for_segment(s),
        ))

    # Then cube faces over the pit.
    for fdata in faces:
        pts = shifted_points(fdata["points"], min_x, min_y)
        body.append(svg_poly(pts, f"cube {fdata['name']} {fdata['shade']}"))

    svg_parts = svg_document(
        width,
        height,
        body,
        "Lab 011 off-side cube in perspective pit",
        "off-side cube in perspective pit",
    )

    (CAPTURES / "blockout_pit_with_red_cube.svg").write_text("\n".join(svg_parts), encoding="utf-8")

def main() -> None:
    ensure_generated()

    intent = json.loads((ROOT / "goal" / "renderer_intent.json").read_text(encoding="utf-8"))
    segments = json.loads((DIST / "pit_line_segments.json").read_text(encoding="utf-8"))

    if intent["projection"].get("type") != "top_down_perspective_rings":
        raise SystemExit("Single-cube polygon proof requires top_down_perspective_rings")

    cube, faces = cube_faces(intent)

    CAPTURES.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)

    write_cube_only_svg(faces)
    write_pit_with_cube_svg(faces, segments)

    json_path = DIST / "single_cube_polygon_faces.json"
    json_path.write_text(json.dumps({
        "source": "goal/renderer_intent.json",
        "projection": intent["projection"]["type"],
        "purpose": "off-side single cube solid red shaded polygon proof in perspective pit before C64 bitmap/span fill",
        "cube": cube,
        "palette": {
            "red_light": "#ff4a3d",
            "red_mid": "#d92f2b",
            "red_mid_dark": "#b32124",
            "red_dark": "#8f171d",
            "red_deep": "#661016",
        },
        "faces": faces,
        "context_svg": "captures/blockout_pit_with_red_cube.svg",
    }, indent=2) + "\n", encoding="utf-8")

    print("Wrote captures/blockout_single_cube_polygon_preview.svg")
    print("Wrote captures/blockout_single_cube_red_shaded_faces.svg")
    print("Wrote captures/blockout_pit_with_red_cube.svg")
    print(f"Wrote {json_path}")
    print("Generated off-side solid red shaded cube in perspective pit.")

if __name__ == "__main__":
    main()
