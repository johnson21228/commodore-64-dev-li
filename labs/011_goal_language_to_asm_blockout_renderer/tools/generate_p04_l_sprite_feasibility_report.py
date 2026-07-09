#!/usr/bin/env python3
from __future__ import annotations

import importlib.util, json, math
from collections import Counter, defaultdict
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
BASE_BUILDER = LAB / "tools" / "build_p02_domino_top_endpoint_preview_prg.py"
OUT = LAB / "dist" / "pieces" / "P04_L.sprite_feasibility_report.json"
SPRITE_W, SPRITE_H, SPRITE_BYTES, MAX_SPRITES = 24, 21, 64, 8

P04_L_Z_STATES = {
    "z_rotation_000": [(1, 1, 0), (2, 1, 0), (3, 1, 0), (1, 2, 0)],
    "z_rotation_090": [(3, 1, 0), (3, 2, 0), (3, 3, 0), (2, 1, 0)],
    "z_rotation_180": [(1, 3, 0), (2, 3, 0), (3, 3, 0), (3, 2, 0)],
    "z_rotation_270": [(1, 1, 0), (1, 2, 0), (1, 3, 0), (2, 3, 0)],
}

def load_base():
    spec = importlib.util.spec_from_file_location("blockout_base_projection", BASE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load base builder: {BASE_BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def segments_for_cells(base, cells):
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
    for x,y,z in cells:
        for (dx,dy,dz), corners in face_defs:
            if (x+dx,y+dy,z+dz) in occupied:
                continue
            verts = [(x+cx,y+cy,z+cz) for cx,cy,cz in corners]
            for i in range(4):
                edges.add(tuple(sorted([verts[i], verts[(i+1)%4]])))
    out = []
    for a,b in sorted(edges):
        x1,y1 = base.project_vertex(a)
        x2,y2 = base.project_vertex(b)
        if (x1,y1) != (x2,y2):
            out.append((x1,y1,x2,y2))
    return sorted(set(out))

def bres(a,b):
    x0,y0=a; x1,y1=b
    pts=[]
    dx=abs(x1-x0); dy=-abs(y1-y0)
    sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1
    err=dx+dy
    while True:
        if 0 <= x0 < 320 and 0 <= y0 < 200:
            pts.append((x0,y0))
        if x0==x1 and y0==y1:
            break
        e2=2*err
        if e2>=dy:
            err += dy; x0 += sx
        if e2<=dx:
            err += dx; y0 += sy
    return pts

def pixels_for_segments(segments):
    pixels=set()
    for x1,y1,x2,y2 in segments:
        pixels.update(bres((x1,y1),(x2,y2)))
    return pixels

def bbox(points):
    xs=[p[0] for p in points]; ys=[p[1] for p in points]
    return {"minX":min(xs),"minY":min(ys),"maxX":max(xs),"maxY":max(ys),
            "width":max(xs)-min(xs)+1,"height":max(ys)-min(ys)+1}

def tile_coverage(points, box):
    ax=(box["minX"]//SPRITE_W)*SPRITE_W
    ay=(box["minY"]//SPRITE_H)*SPRITE_H
    tile_pixels=defaultdict(set)
    for x,y in points:
        tx=(x-ax)//SPRITE_W; ty=(y-ay)//SPRITE_H
        tile_pixels[(tx,ty)].add((x-(ax+tx*SPRITE_W), y-(ay+ty*SPRITE_H)))
    cols=max([t[0] for t in tile_pixels], default=-1)+1
    rows=max([t[1] for t in tile_pixels], default=-1)+1
    return {
        "anchorX": ax, "anchorY": ay,
        "cols": cols, "rows": rows,
        "occupiedTileCount": len(tile_pixels),
        "rectangularTileCount": cols*rows,
        "uniqueTileMaskCount": len({tuple(sorted(v)) for v in tile_pixels.values()}),
        "occupiedTiles": [
            {"tileX":tx,"tileY":ty,"spriteX":ax+tx*SPRITE_W,"spriteY":ay+ty*SPRITE_H,
             "pixelCount":len(tile_pixels[(tx,ty)])}
            for tx,ty in sorted(tile_pixels)
        ],
    }

def slope_bucket(seg):
    x1,y1,x2,y2=seg
    dx=x2-x1; dy=y2-y1
    if dy==0: return "horizontal"
    if dx==0: return "vertical"
    angle=math.degrees(math.atan2(dy,dx))
    if -20 <= angle <= 20 or angle >= 160 or angle <= -160: return "near_horizontal"
    if 70 <= angle <= 110 or -110 <= angle <= -70: return "near_vertical"
    return "diagonal_positive" if angle > 0 else "diagonal_negative"

def segment_analysis(segments):
    buckets=Counter(slope_bucket(s) for s in segments)
    lengths=[round(math.hypot(s[2]-s[0], s[3]-s[1]),2) for s in segments]
    return {"segmentCount":len(segments),"slopeBuckets":dict(buckets),
            "minLength":min(lengths) if lengths else 0,
            "maxLength":max(lengths) if lengths else 0,
            "avgLength":round(sum(lengths)/len(lengths),2) if lengths else 0}

def classify(n):
    return "GOOD" if n <= 4 else "WATCH" if n <= 6 else "MAX" if n <= 8 else "CONFLICT"

def primitive_assessment():
    return {
        "canRepeatSpritesForLongStraightStretches": True,
        "repeatSpriteUse": "Possible for repeated horizontal/vertical/near-axis strokes if projected edges are quantized into reusable 24x21 line fragments.",
        "cornerSprites": "Possible for common elbow/junction/corner motifs, but perspective projection creates multiple slopes and lengths.",
        "recommendedFirstApproach": "Tile each full active-block pose into sprite masks first; then mine repeated tile masks and line/corner motifs.",
        "whyNotOneSpritePerCubeEdge": "A cube has 12 edges and a multi-cube block has many exposed/projected edges. The C64 only has 8 hardware sprites, so edge-per-sprite is over budget immediately.",
        "betterMentalModel": "Sprites are white overlay tiles covering occupied screen regions, not semantic cube-edge objects."
    }

def main():
    base=load_base()
    poses=[]; max_occ=0; max_rect=0
    for state_id,cells in P04_L_Z_STATES.items():
        segs=segments_for_cells(base,cells)
        pts=pixels_for_segments(segs)
        box=bbox(pts)
        tiles=tile_coverage(pts,box)
        max_occ=max(max_occ,tiles["occupiedTileCount"])
        max_rect=max(max_rect,tiles["rectangularTileCount"])
        poses.append({
            "stateId":state_id,
            "occupiedCells":cells,
            "boundingBox":box,
            "pixels":len(pts),
            "segmentAnalysis":segment_analysis(segs),
            "spriteTileCoverage":tiles,
            "classificationByOccupiedTiles":classify(tiles["occupiedTileCount"]),
            "classificationByRectangularGrid":classify(tiles["rectangularTileCount"]),
            "estimatedSpriteBytesOccupiedOnly":tiles["occupiedTileCount"]*SPRITE_BYTES,
            "estimatedSpriteBytesRectangularGrid":tiles["rectangularTileCount"]*SPRITE_BYTES,
        })
    report={
        "schemaVersion":1,
        "pieceId":"P04_L",
        "reportType":"sprite feasibility",
        "sourcePiece":{"pieceId":"P04_L","canonicalCubes":[[0,0,0],[1,0,0],[2,0,0],[0,1,0]],
                       "description":"Four-cube long L from blockout_piece_source.json"},
        "hardwareFacts":{"standardSpriteWidthPixels":SPRITE_W,"standardSpriteHeightPixels":SPRITE_H,
                         "standardSpriteBytes":SPRITE_BYTES,"hardwareSpritesAvailable":MAX_SPRITES,
                         "activeBlockTargetColor":"white","pitTargetLayer":"green bitmap/static layer"},
        "summary":{"poseCount":len(poses),"maxOccupiedSpriteTilesPerPose":max_occ,
                   "maxRectangularGridSpriteTilesPerPose":max_rect,
                   "classificationOccupiedOnly":classify(max_occ),
                   "classificationRectangularGrid":classify(max_rect),
                   "maxOccupiedOnlySpriteBytesPerPose":max_occ*SPRITE_BYTES,
                   "maxRectangularGridSpriteBytesPerPose":max_rect*SPRITE_BYTES,
                   "recommendation":"Use sprite overlay for active block as a serious next experiment. Start with full-pose sprite tiles, not edge-per-sprite. Then evaluate reusable line/corner motif sprites after seeing tile-mask repetition."},
        "primitiveReuseAssessment":primitive_assessment(),
        "poses":poses,
        "nextExperiment":{"name":"green pit bitmap plus white P04_L sprite overlay",
                          "goal":"Avoid hi-res bitmap 8x8 color-cell contamination and remove active block full-screen redraw.",
                          "firstRuntimeScope":["draw green pit once in bitmap","load one P04_L sprite-tile pose","enable white sprites","swap sprite payloads on rotation keys"],
                          "knownRisks":["If a pose needs more than 8 sprite tiles, it exceeds hardware sprite count without multiplexing or smaller projection.",
                                        "Sprite X positions beyond 255 require the VIC sprite X high-bit register.",
                                        "Repeated line/corner primitives need quantization before they become reliable."]}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(report["summary"], indent=2))
    print(json.dumps(report["primitiveReuseAssessment"], indent=2))
if __name__ == "__main__":
    main()
