#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import math
from collections import Counter
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"

CANONICAL = [(0,0,0), (1,0,0), (0,1,0)]
ANCHOR = (0, 0, 0)
KEYS = {
    "A": ("x", 1),
    "Q": ("x", -1),
    "S": ("y", 1),
    "W": ("y", -1),
    "D": ("z", 1),
    "E": ("z", -1),
}

# Conservative byte estimates for C64-friendly endpoint/line-command payloads.
# Format A: x1,y1,x2,y2 per line = 4 bytes.
# Format B: dx/dy/opcode compact line not yet used in report.
ENDPOINT_BYTES_PER_LINE = 4
POSE_HEADER_BYTES = 3  # lineCount + whiteCellCount/seam flag placeholder
TRANSITION_BYTES_PER_ORIENTATION = 6  # A,Q,S,W,D,E nextOrientationId
ORIENTATION_OFFSET_BYTES = 2
GLOBAL_HEADER_BYTES = 16

def load_base():
    spec = importlib.util.spec_from_file_location("blockout_true_axis_endpoint_base", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base builder: {BASE_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def normalize(cells):
    minx = min(x for x, _, _ in cells)
    miny = min(y for _, y, _ in cells)
    minz = min(z for _, _, z in cells)
    return tuple(sorted((x-minx, y-miny, z-minz) for x, y, z in cells))

def rotate_cell(cell, axis, direction):
    x, y, z = cell
    if axis == "x":
        return (x, -z, y) if direction > 0 else (x, z, -y)
    if axis == "y":
        return (z, y, -x) if direction > 0 else (-z, y, x)
    if axis == "z":
        return (-y, x, z) if direction > 0 else (y, -x, z)
    raise ValueError(axis)

def rotate_shape(shape, axis, direction):
    return normalize([rotate_cell(c, axis, direction) for c in shape])

def generate_orientations():
    start = normalize(CANONICAL)
    seen = {start}
    frontier = [start]
    while frontier:
        current = frontier.pop(0)
        for axis in ["x", "y", "z"]:
            for direction in [1, -1]:
                nxt = rotate_shape(current, axis, direction)
                if nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
    shapes = sorted(seen)
    id_by_shape = {shape: idx for idx, shape in enumerate(shapes)}
    transitions = {}
    for idx, shape in enumerate(shapes):
        transitions[idx] = {}
        for key, (axis, direction) in KEYS.items():
            transitions[idx][key] = id_by_shape[rotate_shape(shape, axis, direction)]
    return shapes, transitions

def place_shape(shape):
    ax, ay, az = ANCHOR
    # P03_ELBOW is a three-cube L with max footprint width 2 in any normalized axis.
    # Keep it at the 3x3 pit opening without the previous 5x5 centering shift.
    return sorted((x + ax, y + ay, z + az) for x, y, z in shape)

def exposed_edges_for_cells(cells):
    occupied = set(cells)
    face_defs = [
        ((-1,0,0), [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]),
        ((1,0,0), [(1,0,0),(1,0,1),(1,1,1),(1,1,0)]),
        ((0,-1,0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
        ((0,1,0), [(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
        ((0,0,-1), [(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
        ((0,0,1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
    ]
    edges = set()
    for x, y, z in cells:
        for (dx, dy, dz), corners in face_defs:
            if (x+dx, y+dy, z+dz) in occupied:
                continue
            verts = [(x+cx, y+cy, z+cz) for cx, cy, cz in corners]
            for i in range(4):
                edges.add(tuple(sorted([verts[i], verts[(i+1) % 4]])))
    return sorted(edges)

def projected_segments(base, cells):
    segs = []
    for a, b in exposed_edges_for_cells(cells):
        x1, y1 = base.project_vertex(a)
        x2, y2 = base.project_vertex(b)
        if (x1, y1) != (x2, y2):
            segs.append((x1, y1, x2, y2))
    return sorted(set(segs))

def slope_bucket(seg):
    x1, y1, x2, y2 = seg
    dx = x2 - x1
    dy = y2 - y1
    if dy == 0:
        return "horizontal"
    if dx == 0:
        return "vertical"
    angle = math.degrees(math.atan2(dy, dx))
    if -20 <= angle <= 20 or angle >= 160 or angle <= -160:
        return "near_horizontal"
    if 70 <= angle <= 110 or -110 <= angle <= -70:
        return "near_vertical"
    return "diagonal_positive" if angle > 0 else "diagonal_negative"

def bbox(segs):
    xs = []
    ys = []
    for x1, y1, x2, y2 in segs:
        xs.extend([x1, x2])
        ys.extend([y1, y2])
    return {
        "minX": min(xs), "minY": min(ys), "maxX": max(xs), "maxY": max(ys),
        "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1,
    }

def classify(total_bytes):
    if total_bytes <= 8192:
        return "PATCH"
    if total_bytes <= 16384:
        return "WATCH"
    if total_bytes <= 24576:
        return "MAX"
    return "CONFLICT"

def main():
    base = load_base()
    shapes, transitions = generate_orientations()
    orientations = []
    total_lines = 0
    max_lines = 0
    slope_total = Counter()

    for idx, shape in enumerate(shapes):
        placed = place_shape(shape)
        segs = projected_segments(base, placed)
        slope_counts = Counter(slope_bucket(s) for s in segs)
        lengths = [round(math.hypot(s[2]-s[0], s[3]-s[1]), 2) for s in segs]
        line_count = len(segs)
        total_lines += line_count
        max_lines = max(max_lines, line_count)
        slope_total.update(slope_counts)
        payload_bytes = POSE_HEADER_BYTES + line_count * ENDPOINT_BYTES_PER_LINE
        orientations.append({
            "orientationId": idx,
            "normalizedCells": [list(c) for c in shape],
            "placedCells": [list(c) for c in placed],
            "projectedLineSegmentCount": line_count,
            "estimatedEndpointBytes": payload_bytes,
            "boundingBox": bbox(segs),
            "slopeBuckets": dict(slope_counts),
            "minLength": min(lengths) if lengths else 0,
            "maxLength": max(lengths) if lengths else 0,
            "avgLength": round(sum(lengths) / len(lengths), 2) if lengths else 0,
            "segments": [
                {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
                for x1, y1, x2, y2 in segs
            ],
        })

    orientation_payload_bytes = sum(o["estimatedEndpointBytes"] for o in orientations)
    transition_bytes = len(shapes) * TRANSITION_BYTES_PER_ORIENTATION
    offset_table_bytes = len(shapes) * ORIENTATION_OFFSET_BYTES
    total_estimated = GLOBAL_HEADER_BYTES + offset_table_bytes + transition_bytes + orientation_payload_bytes

    report = {
        "schemaVersion": 1,
        "pieceId": "P03_ELBOW",
        "reportType": "true-axis endpoint 3x3 green-line pit payload report",
        "renderingProblem": "Use a maximum-width-2 three-cube L block so it fits naturally in a 3x3x10 pit.",
        "previousConflict": {
            "fullBitmapObservedProgramBytes": 43695,
            "availablePrgImageBytes": 30719,
            "result": "CONFLICT",
        },
        "payloadStrategy": {
            "name": "endpoint/line-command payload for P03_ELBOW in 3x3x10 pit",
            "endpointBytesPerLine": ENDPOINT_BYTES_PER_LINE,
            "poseHeaderBytes": POSE_HEADER_BYTES,
            "transitionBytesPerOrientation": TRANSITION_BYTES_PER_ORIENTATION,
            "orientationOffsetBytes": ORIENTATION_OFFSET_BYTES,
            "globalHeaderBytes": GLOBAL_HEADER_BYTES,
            "runtimeContract": "C64 runtime looks up orientation transitions and draws prepared endpoint line commands.",
        },
        "axisControls": {"A": "+x", "Q": "-x", "S": "+y", "W": "-y", "D": "+z", "E": "-z"},
        "abovePit": True,
        "pitDimensions": {"widthCells": 3, "heightCells": 3, "depthCells": 10},
        "pitStyle": "green projected boundary/grid lines",
        "floorLines": False,
        "anchor": list(ANCHOR),
        "orientationCount": len(shapes),
        "summary": {
            "orientationCount": len(shapes),
            "totalProjectedLineSegments": total_lines,
            "maxProjectedLineSegmentsPerOrientation": max_lines,
            "orientationPayloadBytes": orientation_payload_bytes,
            "transitionTableBytes": transition_bytes,
            "orientationOffsetTableBytes": offset_table_bytes,
            "globalHeaderBytes": GLOBAL_HEADER_BYTES,
            "estimatedTotalEndpointPayloadBytes": total_estimated,
            "classification": classify(total_estimated),
            "slopeBuckets": dict(slope_total),
            "recommendation": "Proceed to a P03_ELBOW true-axis green-line-pit preview PRG using a small runtime line drawer if classification is PATCH or WATCH.",
        },
        "transitions": {str(k): v for k, v in transitions.items()},
        "orientations": orientations,
        "liPlusPlusMeaning": "Workbench generates the 24-orientation graph and compact endpoint payload; the C64 executes table lookup and line drawing.",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(report["summary"], indent=2))

if __name__ == "__main__":
    main()
