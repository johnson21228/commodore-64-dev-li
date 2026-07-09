#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
PIECE_SOURCE = LAB / "source" / "blockout_piece_source.json"
POSE_RULES = LAB / "source" / "blockout_pose_rules.json"
RAW_REPORT_PATH = LAB / "dist" / "pieces" / "P02_DOMINO.payload_report.json"
REPORT_PATH = LAB / "dist" / "pieces" / "P02_DOMINO.endpoint_payload_report.json"
MANIFEST_PATH = LAB / "dist" / "pieces_manifest.json"

PIT_WIDTH = 5
PIT_HEIGHT = 5
PIT_DEPTH = 10

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
        rotations["source"] = [cube_tuple(cube) for cube in (piece.get("cubes") or piece.get("cells"))]

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

def projected_segments(edges: list[tuple[tuple[int, int, int], tuple[int, int, int]]]) -> list[tuple[int, int, int, int]]:
    segments = []
    for a, b in edges:
        x1, y1 = project_vertex(a)
        x2, y2 = project_vertex(b)
        if (x1, y1) != (x2, y2):
            segments.append((x1, y1, x2, y2))
    return sorted(set(segments))

def bbox(segments: list[tuple[int, int, int, int]]) -> dict[str, int]:
    xs = []
    ys = []
    for x1, y1, x2, y2 in segments:
        xs.extend([x1, x2])
        ys.extend([y1, y2])
    return {
        "minX": max(0, min(xs) if xs else 0),
        "minY": max(0, min(ys) if ys else 0),
        "maxX": min(319, max(xs) if xs else 0),
        "maxY": min(199, max(ys) if ys else 0),
    }

def dirty_cells_from_bbox(box: dict[str, int]) -> int:
    min_cell_x = box["minX"] // 8
    max_cell_x = box["maxX"] // 8
    min_cell_y = box["minY"] // 8
    max_cell_y = box["maxY"] // 8
    return (max_cell_x - min_cell_x + 1) * (max_cell_y - min_cell_y + 1)

def build_report() -> dict[str, Any]:
    source = load_json(PIECE_SOURCE)
    piece = find_piece(source, "P02_DOMINO")
    rotations = extract_rotations(piece)

    missing = [rid for rid in INCLUDED_ROTATIONS if rid not in rotations]
    if missing:
        raise ValueError(f"P02_DOMINO missing rotations: {missing}. Available: {sorted(rotations)}")

    raw_summary = None
    if RAW_REPORT_PATH.exists():
        raw = load_json(RAW_REPORT_PATH)
        raw_summary = raw.get("summary", {})

    poses = []
    rotation_summaries = []
    totals = {
        "poseCount": 0,
        "occupiedCellRecords": 0,
        "exposedEdgeRecords": 0,
        "projectedLineSegments": 0,
        "estimatedPoseHeaderBytes": 0,
        "estimatedOccupiedCellBytes": 0,
        "estimatedEndpointSegmentBytes": 0,
        "estimatedDirtyBBoxBytes": 0,
        "estimatedDirtyColorBBoxBytes": 0,
        "estimatedGridReferenceBytes": 0,
    }
    maxes = {
        "maxProjectedLineSegmentsPerPose": 0,
        "maxEstimatedEndpointBytesPerPose": 0,
        "maxEstimatedGridReferenceBytesPerPose": 0,
        "maxDirtyColorCellsByBBoxPerPose": 0,
    }

    for rid in INCLUDED_ROTATIONS:
        local = normalize(rotations[rid])
        ext = extent(local)
        x_count = PIT_WIDTH - ext["width"] + 1
        y_count = PIT_HEIGHT - ext["height"] + 1
        z_count = PIT_DEPTH - ext["depth"] + 1

        rotation_total = {
            "rotationId": rid,
            "extent": ext,
            "xRange": [0, x_count - 1],
            "yRange": [0, y_count - 1],
            "zRange": [0, z_count - 1],
            "poseCount": x_count * y_count * z_count,
            "projectedLineSegments": 0,
            "estimatedEndpointPayloadBytes": 0,
            "estimatedGridReferencePayloadBytes": 0,
        }

        for z in range(z_count):
            for y in range(y_count):
                for x in range(x_count):
                    world = sorted((x + cx, y + cy, z + cz) for cx, cy, cz in local)
                    edges = exposed_edges(world)
                    segments = projected_segments(edges)
                    box = bbox(segments)
                    dirty_color_cells = dirty_cells_from_bbox(box)

                    segment_count = len(segments)
                    occupied_count = len(world)
                    edge_count = len(edges)

                    # Endpoint format estimate:
                    # - pose header: 12 bytes
                    # - occupied cells: 3 bytes each
                    # - endpoint segment: 4 bytes (x1,y1,x2,y2, all under 256 in current projection)
                    # - dirty bitmap bounding box: 4 bytes
                    # - dirty color-cell bounding box: 4 bytes
                    endpoint_bytes = 12 + occupied_count * 3 + segment_count * 4 + 4 + 4

                    # Grid-reference format estimate:
                    # - pose header: 12 bytes
                    # - occupied cells: 3 bytes each
                    # - edge reference: 2 bytes each
                    # - dirty bitmap/color bounding boxes: 8 bytes
                    # This assumes runtime can project/draw from a per-depth 6x6 vertex grid table.
                    grid_ref_bytes = 12 + occupied_count * 3 + edge_count * 2 + 8

                    poses.append({
                        "poseId": f"P02_DOMINO:{rid}:x{x}:y{y}:z{z}",
                        "pieceId": "P02_DOMINO",
                        "rotationId": rid,
                        "x": x,
                        "y": y,
                        "z": z,
                        "occupiedCells": world,
                        "extent": ext,
                        "exposedEdgeCount": edge_count,
                        "projectedLineSegmentCount": segment_count,
                        "dirtyBoundingBox": box,
                        "dirtyColorCellsByBoundingBox": dirty_color_cells,
                        "estimatedEndpointPayloadBytes": endpoint_bytes,
                        "estimatedGridReferencePayloadBytes": grid_ref_bytes,
                    })

                    totals["poseCount"] += 1
                    totals["occupiedCellRecords"] += occupied_count
                    totals["exposedEdgeRecords"] += edge_count
                    totals["projectedLineSegments"] += segment_count
                    totals["estimatedPoseHeaderBytes"] += 12
                    totals["estimatedOccupiedCellBytes"] += occupied_count * 3
                    totals["estimatedEndpointSegmentBytes"] += segment_count * 4
                    totals["estimatedDirtyBBoxBytes"] += 4
                    totals["estimatedDirtyColorBBoxBytes"] += 4
                    totals["estimatedGridReferenceBytes"] += edge_count * 2

                    rotation_total["projectedLineSegments"] += segment_count
                    rotation_total["estimatedEndpointPayloadBytes"] += endpoint_bytes
                    rotation_total["estimatedGridReferencePayloadBytes"] += grid_ref_bytes

                    maxes["maxProjectedLineSegmentsPerPose"] = max(maxes["maxProjectedLineSegmentsPerPose"], segment_count)
                    maxes["maxEstimatedEndpointBytesPerPose"] = max(maxes["maxEstimatedEndpointBytesPerPose"], endpoint_bytes)
                    maxes["maxEstimatedGridReferenceBytesPerPose"] = max(maxes["maxEstimatedGridReferenceBytesPerPose"], grid_ref_bytes)
                    maxes["maxDirtyColorCellsByBBoxPerPose"] = max(maxes["maxDirtyColorCellsByBBoxPerPose"], dirty_color_cells)

        rotation_summaries.append(rotation_total)

    endpoint_total = (
        totals["estimatedPoseHeaderBytes"]
        + totals["estimatedOccupiedCellBytes"]
        + totals["estimatedEndpointSegmentBytes"]
        + totals["estimatedDirtyBBoxBytes"]
        + totals["estimatedDirtyColorBBoxBytes"]
    )
    grid_reference_total = (
        totals["estimatedPoseHeaderBytes"]
        + totals["estimatedOccupiedCellBytes"]
        + totals["estimatedGridReferenceBytes"]
        + totals["estimatedDirtyBBoxBytes"]
        + totals["estimatedDirtyColorBBoxBytes"]
    )

    if endpoint_total <= 24 * 1024:
        endpoint_decision = "PATCH"
    elif endpoint_total <= 48 * 1024:
        endpoint_decision = "WATCH"
    elif endpoint_total <= 80 * 1024:
        endpoint_decision = "WAIT"
    else:
        endpoint_decision = "CONFLICT"

    if grid_reference_total <= 24 * 1024:
        grid_decision = "PATCH"
    elif grid_reference_total <= 48 * 1024:
        grid_decision = "WATCH"
    elif grid_reference_total <= 80 * 1024:
        grid_decision = "WAIT"
    else:
        grid_decision = "CONFLICT"

    raw_bytes = raw_summary.get("estimatedTotalPayloadBytes") if raw_summary else None

    return {
        "schemaVersion": 1,
        "reportType": "blockout_piece_endpoint_payload_report",
        "pieceId": "P02_DOMINO",
        "purpose": "Compare compact dynamic-block endpoint/topology strategies after raw byte/mask report classified as CONFLICT.",
        "sourceInputs": {
            "pieceSource": str(PIECE_SOURCE),
            "pieceSourceSha256": sha256(PIECE_SOURCE),
            "poseRules": str(POSE_RULES),
            "poseRulesSha256": sha256(POSE_RULES) if POSE_RULES.exists() else None,
            "rawByteMaskReport": str(RAW_REPORT_PATH) if RAW_REPORT_PATH.exists() else None,
            "rawByteMaskReportSha256": sha256(RAW_REPORT_PATH) if RAW_REPORT_PATH.exists() else None,
        },
        "scope": {
            "includedRotations": INCLUDED_ROTATIONS,
            "excludedRotations": EXCLUDED_ROTATIONS,
            "pit": {"width": PIT_WIDTH, "height": PIT_HEIGHT, "depth": PIT_DEPTH},
            "runtimeDrawingIncluded": False,
            "binaryPayloadIncluded": False,
            "zAxisIncluded": False,
            "strategy": "endpoint_and_grid_reference_estimator",
        },
        "estimatedRecordFormats": {
            "endpointSegmentFormat": {
                "poseHeaderBytes": 12,
                "occupiedCellBytes": 3,
                "projectedSegmentBytes": 4,
                "dirtyBitmapBoundingBoxBytes": 4,
                "dirtyColorBoundingBoxBytes": 4,
                "runtimeTradeoff": "Runtime draws line segments from prepared screen endpoints."
            },
            "gridReferenceFormat": {
                "poseHeaderBytes": 12,
                "occupiedCellBytes": 3,
                "edgeReferenceBytes": 2,
                "dirtyBitmapBoundingBoxBytes": 4,
                "dirtyColorBoundingBoxBytes": 4,
                "runtimeTradeoff": "Runtime resolves edge references through a per-depth projected vertex grid, then draws lines."
            }
        },
        "rotationSummaries": rotation_summaries,
        "summary": {
            **totals,
            **maxes,
            "estimatedEndpointPayloadBytes": endpoint_total,
            "estimatedGridReferencePayloadBytes": grid_reference_total,
            "endpointDecisionClassification": endpoint_decision,
            "gridReferenceDecisionClassification": grid_decision,
            "rawByteMaskEstimatedBytes": raw_bytes,
            "endpointSavingsVsRawBytes": (raw_bytes - endpoint_total) if raw_bytes is not None else None,
            "gridReferenceSavingsVsRawBytes": (raw_bytes - grid_reference_total) if raw_bytes is not None else None,
            "recommendation": (
                "Use endpoint or grid-reference dynamic block rendering; do not use full per-pose byte/mask payloads."
                if endpoint_decision in {"PATCH", "WATCH"} or grid_decision in {"PATCH", "WATCH"}
                else "Continue representation work before runtime drawing."
            ),
        },
        "poses": poses,
    }

def update_manifest(report: dict[str, Any]) -> None:
    if MANIFEST_PATH.exists():
        manifest = load_json(MANIFEST_PATH)
    else:
        manifest = {"schemaVersion": 1, "manifestType": "blockout_piece_payload_manifest", "pieces": []}

    pieces = [p for p in manifest.get("pieces", []) if p.get("pieceId") != "P02_DOMINO"]
    pieces.append({
        "pieceId": "P02_DOMINO",
        "rawByteMaskReport": "pieces/P02_DOMINO.payload_report.json",
        "endpointPayloadReport": "pieces/P02_DOMINO.endpoint_payload_report.json",
        "binaryPayload": None,
        "includedRotations": INCLUDED_ROTATIONS,
        "excludedRotations": EXCLUDED_ROTATIONS,
        "poseCount": report["summary"]["poseCount"],
        "estimatedTotalPayloadBytes": report["summary"]["rawByteMaskEstimatedBytes"],
        "rawByteMaskEstimatedBytes": report["summary"]["rawByteMaskEstimatedBytes"],
        "estimatedEndpointPayloadBytes": report["summary"]["estimatedEndpointPayloadBytes"],
        "estimatedGridReferencePayloadBytes": report["summary"]["estimatedGridReferencePayloadBytes"],
        "endpointDecisionClassification": report["summary"]["endpointDecisionClassification"],
        "gridReferenceDecisionClassification": report["summary"]["gridReferenceDecisionClassification"],
    })
    manifest["pieces"] = pieces
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    report = build_report()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    update_manifest(report)
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {MANIFEST_PATH}")
    summary = report["summary"]
    print(f"P02_DOMINO poses: {summary['poseCount']}")
    print(f"Raw byte/mask bytes: {summary['rawByteMaskEstimatedBytes']}")
    print(f"Endpoint payload bytes: {summary['estimatedEndpointPayloadBytes']}")
    print(f"Endpoint decision: {summary['endpointDecisionClassification']}")
    print(f"Grid-reference payload bytes: {summary['estimatedGridReferencePayloadBytes']}")
    print(f"Grid-reference decision: {summary['gridReferenceDecisionClassification']}")
    print(f"Recommendation: {summary['recommendation']}")

if __name__ == "__main__":
    main()
