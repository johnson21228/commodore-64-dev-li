#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSE = ROOT / "source" / "blockout_pose_rules.json"
PIECES = ROOT / "source" / "blockout_piece_source.json"

def norm_tuple(c):
    return tuple(int(v) for v in c)

def extent(cubes):
    xs = [c[0] for c in cubes]
    ys = [c[1] for c in cubes]
    zs = [c[2] for c in cubes]
    return {
        "width": max(xs) - min(xs) + 1,
        "height": max(ys) - min(ys) + 1,
        "depth": max(zs) - min(zs) + 1,
    }

def normalize(cubes):
    xs = [c[0] for c in cubes]
    ys = [c[1] for c in cubes]
    zs = [c[2] for c in cubes]
    mx, my, mz = min(xs), min(ys), min(zs)
    return sorted((x-mx, y-my, z-mz) for x, y, z in cubes)

def face_contiguous(cubes):
    cube_set = set(cubes)
    if not cube_set:
        return False
    start = next(iter(cube_set))
    seen = {start}
    q = deque([start])
    dirs = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    while q:
        x, y, z = q.popleft()
        for dx, dy, dz in dirs:
            n = (x+dx, y+dy, z+dz)
            if n in cube_set and n not in seen:
                seen.add(n)
                q.append(n)
    return seen == cube_set

def load(path):
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))

pose_rules = load(POSE)
pieces = load(PIECES)

if pose_rules.get("kind") != "blockout_pose_rules":
    raise SystemExit(f"Unexpected pose kind: {pose_rules.get('kind')}")
if pose_rules.get("version") != 1:
    raise SystemExit(f"Unexpected pose version: {pose_rules.get('version')}")

pit = pose_rules.get("pit", {})
if pit != {"width": 5, "height": 5, "depth": 10}:
    raise SystemExit(f"Unexpected pit in pose rules: {pit}")

rot_rules = pose_rules.get("rotationRules", {})
if rot_rules.get("runtimePolicy") != "choose_precomputed_rotation_id":
    raise SystemExit(f"Unexpected rotation runtime policy: {rot_rules}")
if rot_rules.get("noRuntimeMatrixMathOnC64") is not True:
    raise SystemExit("Rotation rules must forbid runtime matrix math on C64")
if rot_rules.get("rejectionRule") is None:
    raise SystemExit("Rotation rejection rule missing")

max_extent = rot_rules.get("legality", {}).get("maxExtentAnyAxis")
if max_extent != 3:
    raise SystemExit(f"Unexpected max rotation extent: {max_extent}")

piece_by_id = {p["pieceId"]: p for p in pieces.get("pieces", [])}
if not piece_by_id:
    raise SystemExit("No pieces available for pose verification")

for pid, piece in piece_by_id.items():
    canonical_count = len(piece.get("canonicalCubes", []))
    for rot in piece.get("rotations", []):
        rid = rot["rotationId"]
        cubes = [norm_tuple(c) for c in rot.get("cubes", [])]
        if len(cubes) != canonical_count:
            raise SystemExit(f"{pid}/{rid}: rotation does not preserve cube count")
        if normalize(cubes) != sorted(cubes):
            raise SystemExit(f"{pid}/{rid}: rotation must be normalized to min x/y/z = 0")
        if not face_contiguous(cubes):
            raise SystemExit(f"{pid}/{rid}: rotation is not face-contiguous")
        ex = extent(cubes)
        if max(ex.values()) > max_extent:
            raise SystemExit(f"{pid}/{rid}: extent {ex} exceeds max {max_extent}")
        if ex["width"] == 3 and ex["height"] == 3:
            raise SystemExit(f"{pid}/{rid}: forbidden 3x3 footprint")
        if ex["width"] > pit["width"] or ex["height"] > pit["height"]:
            raise SystemExit(f"{pid}/{rid}: does not fit pit footprint")

first = pose_rules.get("firstOverlayPose", {})
pid = first.get("pieceId")
rid = first.get("rotationId")
pos = first.get("position", {})

if pid not in piece_by_id:
    raise SystemExit(f"firstOverlayPose references unknown pieceId: {first}")

piece = piece_by_id[pid]
rot_by_id = {r["rotationId"]: r for r in piece.get("rotations", [])}
if rid not in rot_by_id:
    raise SystemExit(f"firstOverlayPose references unknown rotationId: {first}")

rot = rot_by_id[rid]
cubes = [norm_tuple(c) for c in rot["cubes"]]
ex = extent(cubes)

for axis in ["x", "y", "z"]:
    if not isinstance(pos.get(axis), int):
        raise SystemExit(f"firstOverlayPose position {axis} must be integer: {first}")

if not (0 <= pos["x"] <= pit["width"] - ex["width"]):
    raise SystemExit(f"firstOverlayPose x out of bounds for extent {ex}: {first}")
if not (0 <= pos["y"] <= pit["height"] - ex["height"]):
    raise SystemExit(f"firstOverlayPose y out of bounds for extent {ex}: {first}")

allowed_z = pose_rules.get("currentOverlayPhase", {}).get("zPolicy", {}).get("allowedZ", [])
if pos["z"] not in allowed_z:
    raise SystemExit(f"firstOverlayPose z not allowed in current overlay phase: {first}")

# Verify all possible rotations have at least one legal x/y placement in the pit.
for pid, piece in piece_by_id.items():
    for rot in piece.get("rotations", []):
        cubes = [norm_tuple(c) for c in rot["cubes"]]
        ex = extent(cubes)
        if pit["width"] - ex["width"] < 0 or pit["height"] - ex["height"] < 0:
            raise SystemExit(f"{pid}/{rot['rotationId']}: no legal placement")

print("OK: Blockout pose and rotation rules verified.")
