#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CAPTURES = ROOT / "captures"
SRC = ROOT / "src"

C64_SHADE_TO_COLOR = {
    "red_light": 2,
    "red_mid": 8,
    "red_mid_dark": 9,
    "red_dark": 11,
    "red_deep": 0,
}

def ensure_projection() -> None:
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

def cube_faces(intent: dict, cube: dict) -> list[dict]:
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

    return [
        face([e, f, b, a], "north_wall", "red_dark"),
        face([f, g, c, b], "east_wall", "red_mid"),
        face([g, h, d, c], "south_wall", "red_deep"),
        face([h, e, a, d], "west_wall", "red_mid_dark"),
        face([a, b, c, d], "top_face", "red_light"),
    ]

def polygon_spans(points: list[dict]) -> list[dict]:
    xy = [(int(p["x"]), int(p["y"])) for p in points]
    min_y = max(0, min(y for x, y in xy))
    max_y = min(199, max(y for x, y in xy))

    spans: list[dict] = []
    for y in range(min_y, max_y + 1):
        intersections: list[float] = []
        for i in range(len(xy)):
            x1, y1 = xy[i]
            x2, y2 = xy[(i + 1) % len(xy)]
            if y1 == y2:
                continue
            low_y = min(y1, y2)
            high_y = max(y1, y2)
            if low_y <= y < high_y:
                t = (y - y1) / (y2 - y1)
                intersections.append(x1 + t * (x2 - x1))
        if len(intersections) < 2:
            continue
        intersections.sort()
        x_start = max(0, round(intersections[0]))
        x_end = min(255, round(intersections[-1]))
        if x_start <= x_end:
            spans.append({"y": y, "x_start": x_start, "x_end": x_end})
    return spans

def frame_for_cube(intent: dict, frame_index: int, cube: dict) -> dict:
    faces = cube_faces(intent, cube)
    frame_faces = []
    total_spans = 0
    total_pixels = 0

    for face_index, face_data in enumerate(faces):
        spans = polygon_spans(face_data["points"])
        total_spans += len(spans)
        total_pixels += sum(span["x_end"] - span["x_start"] + 1 for span in spans)
        frame_faces.append({
            "face_index": face_index,
            "face_name": face_data["name"],
            "shade": face_data["shade"],
            "color_id": C64_SHADE_TO_COLOR[face_data["shade"]],
            "span_count": len(spans),
            "spans": spans,
        })

    return {
        "frame_index": frame_index,
        "cube": cube,
        "faces": faces,
        "span_faces": frame_faces,
        "total_spans": total_spans,
        "total_pixels": total_pixels,
    }

def svg_line(x1: int, y1: int, x2: int, y2: int, klass: str) -> str:
    return f'<line class="{klass}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'

def svg_poly(points: list[dict], klass: str) -> str:
    pts = " ".join(f"{p['x']},{p['y']}" for p in points)
    return f'<polygon class="{klass}" points="{pts}" />'

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

def write_strip_svg(frames: list[dict], pit_segments: list[dict]) -> None:
    # Render a side-by-side preview of same-depth movement positions.
    cell_w = 248
    cell_h = 184
    margin = 16
    width = cell_w * len(frames)
    height = cell_h

    def shift_point(p: dict, frame_index: int) -> tuple[int, int]:
        return p["x"] - 36 + frame_index * cell_w + margin, p["y"] - 6

    body: list[str] = []

    for frame in frames:
        fi = frame["frame_index"]

        for s in pit_segments:
            x1 = s["x1"] - 36 + fi * cell_w + margin
            y1 = s["y1"] - 6
            x2 = s["x2"] - 36 + fi * cell_w + margin
            y2 = s["y2"] - 6
            body.append(svg_line(x1, y1, x2, y2, class_for_segment(s)))

        for face_data in frame["faces"]:
            pts = []
            for p in face_data["points"]:
                x, y = shift_point(p, fi)
                pts.append({"x": x, "y": y})
            body.append(svg_poly(pts, f"cube {face_data['name']} {face_data['shade']}"))

        cx = 8 + fi * cell_w
        body.append(f'<text class="small" x="{cx}" y="{height - 12}">frame {fi}: x={frame["cube"]["x"]}, y={frame["cube"]["y"]}, z={frame["cube"]["z"]}, spans={frame["total_spans"]}</text>')

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '  <title id="title">Lab 011 same-depth moving cube preview</title>',
        '  <desc id="desc">Same-depth red cube positions across the perspective pit.</desc>',
        '  <style>',
        '    .bg { fill: #11131a; }',
        '    .pit_top { stroke: #f7d85c; stroke-width: 1.2; opacity: 0.75; vector-effect: non-scaling-stroke; }',
        '    .pit_side { stroke: #66d9ef; stroke-width: 0.9; opacity: 0.45; vector-effect: non-scaling-stroke; }',
        '    .pit_depth { stroke: #ff7a7a; stroke-width: 0.9; opacity: 0.6; vector-effect: non-scaling-stroke; }',
        '    .pit_grid { stroke: #9aa0a6; stroke-width: 0.8; opacity: 0.4; vector-effect: non-scaling-stroke; }',
        '    .cube { stroke: #ffcccc; stroke-width: 1.1; vector-effect: non-scaling-stroke; }',
        '    .red_light { fill: #ff4a3d; }',
        '    .red_mid { fill: #d92f2b; }',
        '    .red_mid_dark { fill: #b32124; }',
        '    .red_dark { fill: #8f171d; }',
        '    .red_deep { fill: #661016; }',
        '    .small { fill: #ffe3e3; font: 9px monospace; }',
        '  </style>',
        f'  <rect class="bg" x="0" y="0" width="{width}" height="{height}" />',
        *["  " + item for item in body],
        '</svg>',
        '',
    ]

    (CAPTURES / "blockout_moving_cube_same_depth_preview.svg").write_text("\n".join(svg_parts), encoding="utf-8")

def write_asm(frames: list[dict]) -> None:
    lines = [
        "; GENERATED BY WORKBENCH",
        "; Source: dist/moving_cube_same_depth_frames.json",
        "; Purpose: C64-facing span payloads for same-depth cube movement proof.",
        "; Do not edit by hand.",
        "",
        "moving_cube_frame_count:",
        f"    .byte {len(frames)}",
        "",
        "moving_cube_span_records:",
        "    ; frame_index, face_index, color_id, y, x_start, x_end",
    ]

    total = 0
    for frame in frames:
        lines.append(f"    ; frame={frame['frame_index']} cube={frame['cube']} spans={frame['total_spans']}")
        for face in frame["span_faces"]:
            for span in face["spans"]:
                total += 1
                lines.append(
                    f"    .byte {frame['frame_index']}, {face['face_index']}, {face['color_id']}, {span['y']}, {span['x_start']}, {span['x_end']}"
                )

    lines += [
        "",
        "moving_cube_span_total_count:",
        f"    .word {total}",
        "",
    ]

    (SRC / "generated_moving_cube_spans.s").write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    ensure_projection()

    intent = json.loads((ROOT / "goal" / "renderer_intent.json").read_text(encoding="utf-8"))
    pit_segments = json.loads((DIST / "pit_line_segments.json").read_text(encoding="utf-8"))

    # Same depth, same height, changing x position. y stays fixed so this isolates
    # lateral movement cost at a stable z slice.
    cubes = [
        {"x": 0, "y": 1, "z": 3, "width": 1, "depth": 1, "height": 2, "palette": "solid_red_shaded"},
        {"x": 1, "y": 1, "z": 3, "width": 1, "depth": 1, "height": 2, "palette": "solid_red_shaded"},
        {"x": 2, "y": 1, "z": 3, "width": 1, "depth": 1, "height": 2, "palette": "solid_red_shaded"},
        {"x": 3, "y": 1, "z": 3, "width": 1, "depth": 1, "height": 2, "palette": "solid_red_shaded"},
    ]

    frames = [frame_for_cube(intent, index, cube) for index, cube in enumerate(cubes)]

    max_spans = max(frame["total_spans"] for frame in frames)
    max_pixels = max(frame["total_pixels"] for frame in frames)
    total_span_records = sum(frame["total_spans"] for frame in frames)

    # Conservative estimate for a C64 span-fill loop. Real optimized byte-aligned
    # mask fill can do better, but this is useful as a first bound.
    estimated_naive_pixel_cycles = max_pixels * 30
    estimated_span_setup_cycles = max_spans * 60
    estimated_frame_cycles = estimated_naive_pixel_cycles + estimated_span_setup_cycles

    data = {
        "source": "goal/renderer_intent.json",
        "purpose": "same-depth moving cube span payload and realtime-boundary estimate",
        "movement": "x changes, y/z/depth/height held constant",
        "frame_count": len(frames),
        "max_spans_per_frame": max_spans,
        "max_pixels_per_frame": max_pixels,
        "total_span_records": total_span_records,
        "c64_realtime_estimate": {
            "assumption": "conservative naive pixel set plus span setup estimate",
            "estimated_frame_cycles": estimated_frame_cycles,
            "approx_1mhz_60hz_budget": 16667,
            "approx_1mhz_50hz_budget": 20000,
            "within_60hz_budget": estimated_frame_cycles < 16667,
            "within_50hz_budget": estimated_frame_cycles < 20000,
            "note": "This estimates span drawing only, not full game logic. Bitmap double-buffering or optimized byte-span masks are likely needed for polished realtime."
        },
        "frames": frames,
    }

    DIST.mkdir(parents=True, exist_ok=True)
    CAPTURES.mkdir(parents=True, exist_ok=True)
    SRC.mkdir(parents=True, exist_ok=True)

    (DIST / "moving_cube_same_depth_frames.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    write_strip_svg(frames, pit_segments)
    write_asm(frames)

    print("Wrote dist/moving_cube_same_depth_frames.json")
    print("Wrote src/generated_moving_cube_spans.s")
    print("Wrote captures/blockout_moving_cube_same_depth_preview.svg")
    print(f"Generated {len(frames)} same-depth movement frames.")
    print(f"Max spans/frame: {max_spans}")
    print(f"Max pixels/frame: {max_pixels}")
    print(f"Estimated span-fill cycles/frame: {estimated_frame_cycles}")

if __name__ == "__main__":
    main()
