#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source" / "blockout_piece_source.json"

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

def is_face_contiguous(cubes):
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
            n = (x + dx, y + dy, z + dz)
            if n in cube_set and n not in seen:
                seen.add(n)
                q.append(n)
    return seen == cube_set

def normalize(cubes):
    xs = [c[0] for c in cubes]
    ys = [c[1] for c in cubes]
    zs = [c[2] for c in cubes]
    mx, my, mz = min(xs), min(ys), min(zs)
    return sorted((x-mx, y-my, z-mz) for x, y, z in cubes)

if not SRC.exists():
    raise SystemExit(f"Missing {SRC}")

data = json.loads(SRC.read_text(encoding="utf-8"))

if data.get("kind") != "blockout_piece_source":
    raise SystemExit(f"Unexpected kind: {data.get('kind')}")

constraints = data.get("constraints", {})
min_cubes = constraints.get("minCubeCount")
max_cubes = constraints.get("maxCubeCount")
max_extent = constraints.get("maxExtentAnyAxis")
if min_cubes != 1 or max_cubes != 4 or max_extent != 3:
    raise SystemExit(f"Unexpected piece constraints: {constraints}")

pieces = data.get("pieces", [])
if not pieces:
    raise SystemExit("No piece definitions found")

piece_ids = set()
for piece in pieces:
    pid = piece.get("pieceId")
    if not pid:
        raise SystemExit(f"Piece missing pieceId: {piece}")
    if pid in piece_ids:
        raise SystemExit(f"Duplicate pieceId: {pid}")
    piece_ids.add(pid)

    canonical = [norm_tuple(c) for c in piece.get("canonicalCubes", [])]
    if not (min_cubes <= len(canonical) <= max_cubes):
        raise SystemExit(f"{pid}: cube count {len(canonical)} violates {min_cubes}..{max_cubes}")
    if len(set(canonical)) != len(canonical):
        raise SystemExit(f"{pid}: duplicate canonical cubes")
    if normalize(canonical) != sorted(canonical):
        raise SystemExit(f"{pid}: canonical cubes must be normalized")
    if not is_face_contiguous(canonical):
        raise SystemExit(f"{pid}: canonical cubes are not face-contiguous")

    rotations = piece.get("rotations", [])
    if not rotations:
        raise SystemExit(f"{pid}: missing rotations")

    rot_ids = set()
    for rot in rotations:
        rid = rot.get("rotationId")
        if not rid:
            raise SystemExit(f"{pid}: rotation missing rotationId")
        if rid in rot_ids:
            raise SystemExit(f"{pid}: duplicate rotationId {rid}")
        rot_ids.add(rid)

        cubes = [norm_tuple(c) for c in rot.get("cubes", [])]
        if len(cubes) != len(canonical):
            raise SystemExit(f"{pid}/{rid}: cube count changed")
        if len(set(cubes)) != len(cubes):
            raise SystemExit(f"{pid}/{rid}: duplicate cubes")
        if normalize(cubes) != sorted(cubes):
            raise SystemExit(f"{pid}/{rid}: rotation cubes must be normalized")
        if not is_face_contiguous(cubes):
            raise SystemExit(f"{pid}/{rid}: rotation cubes are not face-contiguous")

        ex = extent(cubes)
        if max(ex.values()) > max_extent:
            raise SystemExit(f"{pid}/{rid}: extent {ex} exceeds max axis extent {max_extent}")
        if ex["width"] == 3 and ex["height"] == 3:
            raise SystemExit(f"{pid}/{rid}: forbidden 3x3 footprint")

        expected_legal = {
            "xMin": 0,
            "xMax": 5 - ex["width"],
            "yMin": 0,
            "yMax": 5 - ex["height"],
        }
        if expected_legal["xMax"] < 0 or expected_legal["yMax"] < 0:
            raise SystemExit(f"{pid}/{rid}: does not fit 5x5 pit")

rendering = data.get("rendering", {})
dirty = rendering.get("dirtyContract", {})
required_dirty_keys = {"bitmapByteOffset", "screenCellOffset", "colorCellOffset"}
if set(dirty.get("dirtyKeys", [])) != required_dirty_keys:
    raise SystemExit(f"Dirty keys do not match expected contract: {dirty.get('dirtyKeys')}")

target = data.get("firstOverlayTarget", {})
if target.get("pieceId") not in piece_ids:
    raise SystemExit(f"firstOverlayTarget references unknown piece: {target}")
target_piece = next(p for p in pieces if p["pieceId"] == target["pieceId"])
target_rots = {r["rotationId"] for r in target_piece["rotations"]}
if target.get("rotationId") not in target_rots:
    raise SystemExit(f"firstOverlayTarget references unknown rotation: {target}")

print(f"OK: Blockout piece source verified ({len(pieces)} pieces, 1..4 cubes, no 3x3 footprint).")
