#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PIECE_SOURCE = LAB / "source" / "blockout_piece_source.json"
POSE_RULES = LAB / "source" / "blockout_pose_rules.json"
REPORT_PATH = LAB / "dist" / "pieces" / "P02_DOMINO.payload_report.json"
MANIFEST_PATH = LAB / "dist" / "pieces_manifest.json"

PIT_WIDTH = 5
PIT_HEIGHT = 5
PIT_DEPTH = 10
BYTES_PER_BITMAP_ROW = 40

# Current Lab 011 pit projection contract.
VIEWPORT = {
    "near": {"left": 30, "top": 2, "right": 226, "bottom": 198},
    "far": {"left": 92, "top": 64, "right": 164, "bottom": 136},
    "depthT": {
        0: 0.00,
        1: 0.34,
        2: 0.56,
        3: 0.71,
        4: 0.81,
        5: 0.88,
        6: 0.93,
        7: 0.96,
        8: 0.98,
        9: 0.99,
        10: 1.00,
    },
}

INCLUDED_ROTATIONS = ["x_axis", "y_axis"]
EXCLUDED_ROTATIONS = ["z_axis"]

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def piece_id(piece: dict[str, Any]) -> str | None:
    value = piece.get("pieceId") or piece.get("id") or piece.get("name")
    return str(value) if value is not None else None

def cube_tuple(cube: Any) -> tuple[int, int, int]:
    if isinstance(cube, dict):
        return (int(cube["x"]), int(cube["y"]), int(cube["z"]))
    if isinstance(cube, (list, tuple)) and len(cube) == 3:
        return (int(cube[0]), int(cube[1]), int(cube[2]))
    raise ValueError(f"Unsupported cube form: {cube!r}")

def rotation_id(rotation: dict[str, Any]) -> str | None:
    value = rotation.get("rotationId") or rotation.get("id") or rotation.get("name")
    return str(value) if value is not None else None

def extract_pieces(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        if isinstance(data.get("pieces"), list):
            return data["pieces"]
        if isinstance(data.get("pieceDefinitions"), list):
            return data["pieceDefinitions"]
    if isinstance(data, list):
        return data
    raise ValueError("Could not find pieces list in piece source")

def find_piece(data: Any, wanted: str) -> dict[str, Any]:
    for piece in extract_pieces(data):
        if piece_id(piece) == wanted:
            return piece
    raise ValueError(f"Could not find piece {wanted}")

def extract_rotations(piece: dict[str, Any]) -> dict[str, list[tuple[int, int, int]]]:
    rotations: dict[str, list[tuple[int, int, int]]] = {}
    raw_rotations = piece.get("rotations") or piece.get("normalizedRotations") or piece.get("rotationDefinitions")

    if isinstance(raw_rotations, list):
        for rotation in raw_rotations:
            rid = rotation_id(rotation)
            cubes = rotation.get("cubes") or rotation.get("cells") or rotation.get("occupancy")
            if rid and cubes:
                rotations[rid] = [cube_tuple(cube) for cube in cubes]

    elif isinstance(raw_rotations, dict):
        for rid, value in raw_rotations.items():
            if isinstance(value, dict):
                cubes = value.get("cubes") or value.get("cells") or value.get("occupancy")
            else:
                cubes = value
            if cubes:
                rotations[str(rid)] = [cube_tuple(cube) for cube in cubes]

    if not rotations and (piece.get("cubes") or piece.get("cells")):
        cubes = [cube_tuple(cube) for cube in (piece.get("cubes") or piece.get("cells"))]
        rotations["source"] = cubes

    return rotations

def normalize(cubes: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    min_x = min(c[0] for c in cubes)
    min_y = min(c[1] for c in cubes)
    min_z = min(c[2] for c in cubes)
    return sorted((x - min_x, y - min_y, z - min_z) for x, y, z in cubes)

def extent(cubes: list[tuple[int, int, int]]) -> dict[str, int]:
    return {
        "width": max(x for x, _, _ in cubes) + 1,
        "height": max(y for _, y, _ in cubes) + 1,
        "depth": max(z for _, _, z in cubes) + 1,
    }

def edge_key(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    return tuple(sorted([a, b]))  # type: ignore[return-value]

FACE_DEFS = [
    ((-1, 0, 0), [(0,0,0),(0,1,0),(0,1,1),(0,0,1)]),
    ((1, 0, 0), [(1,0,0),(1,0,1),(1,1,1),(1,1,0)]),
    ((0, -1, 0), [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
    ((0, 1, 0), [(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
    ((0, 0, -1), [(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
    ((0, 0, 1), [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
]

def exposed_edges(world_cubes: list[tuple[int, int, int]]) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    occupied = set(world_cubes)
    edges = set()
    for x, y, z in world_cubes:
        for (dx, dy, dz), corners in FACE_DEFS:
            if (x + dx, y + dy, z + dz) in occupied:
                continue
            verts = [(x + cx, y + cy, z + cz) for cx, cy, cz in corners]
            for i in range(4):
                edges.add(edge_key(verts[i], verts[(i + 1) % 4]))
    return sorted(edges)

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def project_vertex(v: tuple[int, int, int]) -> tuple[int, int]:
    x, y, z = v
    z = max(0, min(10, z))
    t = VIEWPORT["depthT"][z]
    near = VIEWPORT["near"]
    far = VIEWPORT["far"]
    left = lerp(near["left"], far["left"], t)
    top = lerp(near["top"], far["top"], t)
    right = lerp(near["right"], far["right"], t)
    bottom = lerp(near["bottom"], far["bottom"], t)
    px = round(left + (x / PIT_WIDTH) * (right - left))
    py = round(top + (y / PIT_HEIGHT) * (bottom - top))
    return (int(px), int(py))

def bresenham(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    x0, y0 = a
    x1, y1 = b
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        if 0 <= x0 < 320 and 0 <= y0 < 200:
            points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return points

def byte_mask_records(edges: list[tuple[tuple[int, int, int], tuple[int, int, int]]]) -> dict[int, int]:
    records: dict[int, int] = {}
    for a, b in edges:
        pa = project_vertex(a)
        pb = project_vertex(b)
        for x, y in bresenham(pa, pb):
            offset = y * BYTES_PER_BITMAP_ROW + (x // 8)
            mask = 1 << (7 - (x % 8))
            records[offset] = records.get(offset, 0) | mask
    return records

def color_cells_from_records(records: dict[int, int]) -> list[int]:
    cells = set()
    for offset in records:
        y = offset // BYTES_PER_BITMAP_ROW
        byte_x = offset % BYTES_PER_BITMAP_ROW
        cell_x = byte_x
        cell_y = y // 8
        if 0 <= cell_x < 40 and 0 <= cell_y < 25:
            cells.add(cell_y * 40 + cell_x)
    return sorted(cells)

def build_report() -> dict[str, Any]:
    source = load_json(PIECE_SOURCE)
    piece = find_piece(source, "P02_DOMINO")
    rotations = extract_rotations(piece)

    missing = [rid for rid in INCLUDED_ROTATIONS if rid not in rotations]
    if missing:
        raise ValueError(f"P02_DOMINO missing rotations: {missing}. Available: {sorted(rotations)}")

    poses = []
    rotation_summaries = []
    totals = {
        "poseCount": 0,
        "occupiedCellRecords": 0,
        "exposedEdgeRecords": 0,
        "bitmapByteMaskRecords": 0,
        "dirtyBitmapOffsets": 0,
        "touchedColorCells": 0,
        "estimatedPoseHeaderBytes": 0,
        "estimatedOccupiedCellBytes": 0,
        "estimatedDrawRecordBytes": 0,
        "estimatedDirtyBitmapBytes": 0,
        "estimatedDirtyColorBytes": 0,
    }
    maxes = {
        "maxBitmapByteMaskRecordsPerPose": 0,
        "maxDirtyBitmapOffsetsPerPose": 0,
        "maxTouchedColorCellsPerPose": 0,
        "maxEstimatedBytesPerPose": 0,
    }

    for rid in INCLUDED_ROTATIONS:
        local = normalize(rotations[rid])
        ext = extent(local)
        x_count = PIT_WIDTH - ext["width"] + 1
        y_count = PIT_HEIGHT - ext["height"] + 1
        z_count = PIT_DEPTH - ext["depth"] + 1
        pose_count = x_count * y_count * z_count

        rotation_totals = {
            "rotationId": rid,
            "extent": ext,
            "xRange": [0, x_count - 1],
            "yRange": [0, y_count - 1],
            "zRange": [0, z_count - 1],
            "poseCount": pose_count,
            "bitmapByteMaskRecords": 0,
            "touchedColorCells": 0,
            "estimatedPayloadBytes": 0,
        }

        for z in range(z_count):
            for y in range(y_count):
                for x in range(x_count):
                    world = sorted((x + cx, y + cy, z + cz) for cx, cy, cz in local)
                    edges = exposed_edges(world)
                    records = byte_mask_records(edges)
                    color_cells = color_cells_from_records(records)

                    draw_count = len(records)
                    dirty_bitmap_count = draw_count
                    color_count = len(color_cells)
                    occupied_count = len(world)
                    edge_count = len(edges)

                    # Current estimated compact format:
                    # pose header = 12 bytes
                    # occupied cell = 3 bytes each
                    # draw record = 2-byte bitmap offset + 1-byte mask
                    # dirty bitmap offset = 2 bytes each
                    # dirty color cell offset = 2 bytes each
                    estimated_bytes = (
                        12
                        + occupied_count * 3
                        + draw_count * 3
                        + dirty_bitmap_count * 2
                        + color_count * 2
                    )

                    pose = {
                        "poseId": f"P02_DOMINO:{rid}:x{x}:y{y}:z{z}",
                        "pieceId": "P02_DOMINO",
                        "rotationId": rid,
                        "x": x,
                        "y": y,
                        "z": z,
                        "occupiedCells": world,
                        "extent": ext,
                        "exposedEdgeCount": edge_count,
                        "bitmapByteMaskRecordCount": draw_count,
                        "dirtyBitmapOffsetCount": dirty_bitmap_count,
                        "touchedColorCellCount": color_count,
                        "estimatedPayloadBytes": estimated_bytes,
                    }
                    poses.append(pose)

                    totals["poseCount"] += 1
                    totals["occupiedCellRecords"] += occupied_count
                    totals["exposedEdgeRecords"] += edge_count
                    totals["bitmapByteMaskRecords"] += draw_count
                    totals["dirtyBitmapOffsets"] += dirty_bitmap_count
                    totals["touchedColorCells"] += color_count
                    totals["estimatedPoseHeaderBytes"] += 12
                    totals["estimatedOccupiedCellBytes"] += occupied_count * 3
                    totals["estimatedDrawRecordBytes"] += draw_count * 3
                    totals["estimatedDirtyBitmapBytes"] += dirty_bitmap_count * 2
                    totals["estimatedDirtyColorBytes"] += color_count * 2

                    rotation_totals["bitmapByteMaskRecords"] += draw_count
                    rotation_totals["touchedColorCells"] += color_count
                    rotation_totals["estimatedPayloadBytes"] += estimated_bytes

                    maxes["maxBitmapByteMaskRecordsPerPose"] = max(maxes["maxBitmapByteMaskRecordsPerPose"], draw_count)
                    maxes["maxDirtyBitmapOffsetsPerPose"] = max(maxes["maxDirtyBitmapOffsetsPerPose"], dirty_bitmap_count)
                    maxes["maxTouchedColorCellsPerPose"] = max(maxes["maxTouchedColorCellsPerPose"], color_count)
                    maxes["maxEstimatedBytesPerPose"] = max(maxes["maxEstimatedBytesPerPose"], estimated_bytes)

        rotation_summaries.append(rotation_totals)

    total_payload = (
        totals["estimatedPoseHeaderBytes"]
        + totals["estimatedOccupiedCellBytes"]
        + totals["estimatedDrawRecordBytes"]
        + totals["estimatedDirtyBitmapBytes"]
        + totals["estimatedDirtyColorBytes"]
    )
    totals["estimatedTotalPayloadBytes"] = total_payload

    if total_payload <= 24 * 1024:
        decision = "PATCH"
    elif total_payload <= 48 * 1024:
        decision = "WATCH"
    elif total_payload <= 80 * 1024:
        decision = "WAIT"
    else:
        decision = "CONFLICT"

    return {
        "schemaVersion": 1,
        "reportType": "blockout_piece_payload_report",
        "pieceId": "P02_DOMINO",
        "purpose": "Measure first per-piece active payload target before C64 runtime drawing or file I/O.",
        "sourceInputs": {
            "pieceSource": str(PIECE_SOURCE),
            "pieceSourceSha256": sha256(PIECE_SOURCE),
            "poseRules": str(POSE_RULES),
            "poseRulesSha256": sha256(POSE_RULES) if POSE_RULES.exists() else None,
        },
        "scope": {
            "includedRotations": INCLUDED_ROTATIONS,
            "excludedRotations": EXCLUDED_ROTATIONS,
            "pit": {"width": PIT_WIDTH, "height": PIT_HEIGHT, "depth": PIT_DEPTH},
            "runtimeDrawingIncluded": False,
            "binaryPayloadIncluded": False,
            "zAxisIncluded": False,
        },
        "projection": VIEWPORT,
        "estimatedCompactRecordFormat": {
            "poseHeaderBytes": 12,
            "occupiedCellBytes": 3,
            "drawRecordBytes": 3,
            "dirtyBitmapOffsetBytes": 2,
            "dirtyColorCellOffsetBytes": 2,
            "note": "This is an estimator/report scaffold, not the final binary payload format."
        },
        "rotationSummaries": rotation_summaries,
        "summary": {
            **totals,
            **maxes,
            "decisionClassification": decision,
            "decisionMeaning": {
                "PATCH": "Small enough to proceed toward binary payload scaffold.",
                "WATCH": "Likely viable but size discipline is needed.",
                "WAIT": "Too large for direct runtime work; improve representation first.",
                "CONFLICT": "Violates lean active-payload memory direction."
            }[decision],
        },
        "poses": poses,
    }

def write_manifest(report: dict[str, Any]) -> None:
    manifest = {
        "schemaVersion": 1,
        "manifestType": "blockout_piece_payload_manifest",
        "pieces": [
            {
                "pieceId": "P02_DOMINO",
                "report": "pieces/P02_DOMINO.payload_report.json",
                "binaryPayload": None,
                "includedRotations": INCLUDED_ROTATIONS,
                "excludedRotations": EXCLUDED_ROTATIONS,
                "poseCount": report["summary"]["poseCount"],
                "estimatedTotalPayloadBytes": report["summary"]["estimatedTotalPayloadBytes"],
                "decisionClassification": report["summary"]["decisionClassification"],
            }
        ],
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    report = build_report()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_manifest(report)
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {MANIFEST_PATH}")
    summary = report["summary"]
    print(f"P02_DOMINO poses: {summary['poseCount']}")
    print(f"Estimated payload bytes: {summary['estimatedTotalPayloadBytes']}")
    print(f"Decision: {summary['decisionClassification']} - {summary['decisionMeaning']}")

if __name__ == "__main__":
    main()
