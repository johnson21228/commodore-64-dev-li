#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
OUT = LAB / "dist" / "pieces" / "P03_ELBOW.true_axis_endpoint_3x3_green_line_pit_payload_report.json"

PIT_W = 3
PIT_H = 3
PIT_VISUAL_DEPTH = 10
DEPTH_T_BY_Z = [0.00, 0.34, 0.56, 0.71, 0.81, 0.88, 0.93, 0.96, 0.98, 0.99, 1.00]
PIECE_CELLS = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
POSE_W = 3
POSE_H = 3

def project(x: float, y: float, z: float) -> tuple[int, int]:
    play_y0 = 2
    play_y1 = 198
    pit_size = play_y1 - play_y0
    play_x0 = 30
    play_x1 = play_x0 + pit_size
    z_clamped = max(0.0, min(float(PIT_VISUAL_DEPTH), float(z)))
    z0 = int(z_clamped)
    z1 = min(PIT_VISUAL_DEPTH, z0 + 1)
    frac = z_clamped - z0
    t = DEPTH_T_BY_Z[z0] + (DEPTH_T_BY_Z[z1] - DEPTH_T_BY_Z[z0]) * frac
    near_w = play_x1 - play_x0
    near_h = play_y1 - play_y0
    far_w = 72
    far_h = 72
    width = near_w + (far_w - near_w) * t
    height = near_h + (far_h - near_h) * t
    cx = (play_x0 + play_x1) / 2
    cy = (play_y0 + play_y1) / 2
    left = cx - width / 2
    top = cy - height / 2
    return round(left + x * width / PIT_W), round(top + y * height / PIT_H)

def rot_x(c):
    x, y, z = c
    return (x, -z, y)

def rot_y(c):
    x, y, z = c
    return (z, y, -x)

def rot_z(c):
    x, y, z = c
    return (-y, x, z)

ROTS = {
    "+x": rot_x,
    "-x": lambda c: rot_x(rot_x(rot_x(c))),
    "+y": rot_y,
    "-y": lambda c: rot_y(rot_y(rot_y(c))),
    "+z": rot_z,
    "-z": lambda c: rot_z(rot_z(rot_z(c))),
}

def normalize(cells):
    minx = min(x for x, y, z in cells)
    miny = min(y for x, y, z in cells)
    minz = min(z for x, y, z in cells)
    return tuple(sorted((x - minx, y - miny, z - minz) for x, y, z in cells))

def apply_rot(cells, key):
    return normalize([ROTS[key](c) for c in cells])

def build_orientations():
    start = normalize(PIECE_CELLS)
    seen = {start: 0}
    order = [start]
    q = deque([start])
    transitions = {}
    while q:
        cells = q.popleft()
        idx = seen[cells]
        transitions[str(idx)] = {}
        for key, axis in [("A", "+x"), ("Q", "-x"), ("S", "+y"), ("W", "-y"), ("D", "+z"), ("E", "-z")]:
            nxt = apply_rot(cells, axis)
            if nxt not in seen:
                seen[nxt] = len(order)
                order.append(nxt)
                q.append(nxt)
            transitions[str(idx)][key] = seen[nxt]
    return order, transitions

def dims(cells):
    return (
        max(x for x, y, z in cells) + 1,
        max(y for x, y, z in cells) + 1,
        max(z for x, y, z in cells) + 1,
    )

def place_in_current_pit(cells, cursor_x: int = 0, cursor_y: int = 0):
    width, height, depth = dims(cells)
    max_ox = max(0, PIT_W - width)
    max_oy = max(0, PIT_H - height)
    ox = max(0, min(cursor_x, max_ox))
    oy = max(0, min(cursor_y, max_oy))
    placed = tuple(sorted((x + ox, y + oy, z) for x, y, z in cells))
    for x, y, z in placed:
        if not (0 <= x < PIT_W and 0 <= y < PIT_H and 0 <= z < PIT_VISUAL_DEPTH):
            raise RuntimeError(f"placed P03 cell outside 3x3x10 pit: {(x, y, z)}")
    return placed, ox, oy, max_ox, max_oy

def cube_edges_for_cells(cells):
    edge_set = set()
    for x, y, z in cells:
        def add(a, b):
            edge_set.add(tuple(sorted((a, b))))
        for yy in [0, 1]:
            for zz in [0, 1]:
                add((x, y + yy, z + zz), (x + 1, y + yy, z + zz))
        for xx in [0, 1]:
            for zz in [0, 1]:
                add((x + xx, y, z + zz), (x + xx, y + 1, z + zz))
        for xx in [0, 1]:
            for yy in [0, 1]:
                add((x + xx, y + yy, z), (x + xx, y + yy, z + 1))
    return sorted(edge_set)

def project_edges(cells):
    segments = []
    for a, b in cube_edges_for_cells(cells):
        x1, y1 = project(*a)
        x2, y2 = project(*b)
        segments.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
    segments.sort(key=lambda s: (s["y1"], s["x1"], s["y2"], s["x2"]))
    return segments

def slope_bucket(seg):
    dx = seg["x2"] - seg["x1"]
    dy = seg["y2"] - seg["y1"]
    if dx == 0:
        return "vertical"
    if dy == 0:
        return "horizontal"
    adx = abs(dx)
    ady = abs(dy)
    if abs(adx - ady) <= 2:
        return "diagonal_positive" if dx * dy > 0 else "diagonal_negative"
    return "near_horizontal" if adx > ady else "near_vertical"

def length(seg):
    return math.hypot(seg["x2"] - seg["x1"], seg["y2"] - seg["y1"])

def bbox(segs):
    xs = []
    ys = []
    for s in segs:
        xs += [s["x1"], s["x2"]]
        ys += [s["y1"], s["y2"]]
    return {
        "minX": min(xs), "minY": min(ys),
        "maxX": max(xs), "maxY": max(ys),
        "width": max(xs) - min(xs) + 1,
        "height": max(ys) - min(ys) + 1,
    }

def orientation_record(idx, cells):
    placed, ox, oy, max_ox, max_oy = place_in_current_pit(cells, 0, 0)
    segs = project_edges(placed)
    buckets = {}
    for s in segs:
        buckets[slope_bucket(s)] = buckets.get(slope_bucket(s), 0) + 1
    lens = [length(s) for s in segs]
    width, height, depth = dims(cells)
    return {
        "orientationId": idx,
        "normalizedCells": [list(c) for c in cells],
        "placedCells": [list(c) for c in placed],
        "legalCursor": {"maxX": max_ox, "maxY": max_oy},
        "dimensions": {"widthCells": width, "heightCells": height, "depthCells": depth},
        "projectedLineSegmentCount": len(segs),
        "estimatedEndpointBytes": 1 + len(segs) * 4,
        "boundingBox": bbox(segs),
        "slopeBuckets": buckets,
        "minLength": round(min(lens), 2),
        "maxLength": round(max(lens), 2),
        "avgLength": round(sum(lens) / len(lens), 2),
        "segments": segs,
    }

def pose_payload_record(pose_id, orientation_id, cells, cursor_x, cursor_y):
    placed, ox, oy, max_ox, max_oy = place_in_current_pit(cells, cursor_x, cursor_y)
    segs = project_edges(placed)
    return {
        "poseId": pose_id,
        "orientationId": orientation_id,
        "cursorX": cursor_x,
        "cursorY": cursor_y,
        "clampedX": ox,
        "clampedY": oy,
        "legalCursor": {"maxX": max_ox, "maxY": max_oy},
        "placedCells": [list(c) for c in placed],
        "projectedLineSegmentCount": len(segs),
        "estimatedEndpointBytes": 1 + len(segs) * 4,
        "boundingBox": bbox(segs),
        "segments": segs,
    }

def main():
    orientations, transitions = build_orientations()
    orientation_records = [orientation_record(idx, cells) for idx, cells in enumerate(orientations)]

    pose_payloads = []
    pose_id = 0
    for orientation_id, cells in enumerate(orientations):
        for cursor_y in range(POSE_H):
            for cursor_x in range(POSE_W):
                pose_payloads.append(pose_payload_record(pose_id, orientation_id, cells, cursor_x, cursor_y))
                pose_id += 1

    all_buckets = {}
    total_segments = 0
    max_segments = 0
    for record in pose_payloads:
        total_segments += record["projectedLineSegmentCount"]
        max_segments = max(max_segments, record["projectedLineSegmentCount"])
        for s in record["segments"]:
            b = slope_bucket(s)
            all_buckets[b] = all_buckets.get(b, 0) + 1

    orientation_payload_bytes = sum(1 + len(o["segments"]) * 4 for o in orientation_records)
    pose_payload_bytes = sum(1 + len(p["segments"]) * 4 for p in pose_payloads)
    report = {
        "schemaVersion": 3,
        "pieceId": "P03_ELBOW",
        "reportType": "true-axis endpoint payload report",
        "renderingProblem": "Generate active-block endpoint line payload using the same WASD 3x3x10 projection contract as the pit.",
        "previousConflict": "Origin-pinned block payload did not follow current pit size/projection.",
        "payloadStrategy": "precomputed endpoint line commands; C64 runtime table-selects orientation+cursor pose payloads and draws lines",
        "projectionContract": "WASD_3x3x10",
        "axisControls": {"A": "+x", "Q": "-x", "S": "+y", "W": "-y", "D": "+z", "E": "-z"},
        "translationControls": {
            "cursorLeft": {"getinCodeHex": "0x9D", "delta": [-1, 0]},
            "cursorRight": {"getinCodeHex": "0x1D", "delta": [1, 0]},
            "cursorUp": {"getinCodeHex": "0x91", "delta": [0, -1]},
            "cursorDown": {"getinCodeHex": "0x11", "delta": [0, 1]},
        },
        "abovePit": False,
        "pitDimensions": {"widthCells": PIT_W, "heightCells": PIT_H, "depthCells": PIT_VISUAL_DEPTH},
        "pitStyle": "green dotted pit, 4 dots per visible pit cell edge",
        "floorLines": False,
        "anchor": "runtime-cursor-in-current-3x3-pit",
        "poseGrid": {"width": POSE_W, "height": POSE_H, "poseCount": len(pose_payloads), "indexFormula": "orientationId*9 + cursorY*3 + cursorX"},
        "orientationCount": len(orientation_records),
        "summary": {
            "orientationCount": len(orientation_records),
            "orientationProjectedLineSegments": sum(o["projectedLineSegmentCount"] for o in orientation_records),
            "totalProjectedLineSegments": total_segments,
            "maxProjectedLineSegmentsPerOrientation": max(o["projectedLineSegmentCount"] for o in orientation_records),
            "maxProjectedLineSegmentsPerPose": max_segments,
            "orientationPayloadBytes": orientation_payload_bytes,
            "posePayloadBytes": pose_payload_bytes,
            "transitionTableBytes": len(orientation_records) * 6,
            "orientationOffsetTableBytes": len(pose_payloads) * 2,
            "globalHeaderBytes": 16,
            "estimatedTotalEndpointPayloadBytes": pose_payload_bytes + len(pose_payloads) * 2 + len(orientation_records) * 6 + 16,
            "classification": "PATCH",
            "slopeBuckets": all_buckets,
            "recommendation": "Proceed: P03_ELBOW endpoint payload now shares WASD_3x3x10 projection and supports cursor translation.",
        },
        "transitions": transitions,
        "orientations": orientation_records,
        "posePayloads": pose_payloads,
        "liPlusPlusMeaning": {
            "intelligenceLivesUpstream": True,
            "runtimeStaysLean": True,
            "payloadIsContract": True,
            "screenIsProof": True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(report["summary"], indent=2))

if __name__ == "__main__":
    main()
