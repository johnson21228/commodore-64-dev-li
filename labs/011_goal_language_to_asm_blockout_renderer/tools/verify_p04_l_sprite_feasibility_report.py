#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

LAB = Path("labs/011_goal_language_to_asm_blockout_renderer")
REPORT = LAB / "dist" / "pieces" / "P04_L.sprite_feasibility_report.json"
errors=[]
if not REPORT.exists():
    errors.append(f"Missing report: {REPORT}")
else:
    d=json.loads(REPORT.read_text(encoding="utf-8"))
    if d.get("pieceId")!="P04_L": errors.append("report must be for P04_L")
    if d.get("reportType")!="sprite feasibility": errors.append("reportType must be sprite feasibility")
    hw=d.get("hardwareFacts",{})
    if hw.get("hardwareSpritesAvailable")!=8: errors.append("hardware sprite count must be 8")
    if hw.get("standardSpriteWidthPixels")!=24 or hw.get("standardSpriteHeightPixels")!=21:
        errors.append("standard sprite size must be 24x21")
    s=d.get("summary",{})
    if s.get("poseCount")!=4: errors.append("P04_L report must contain four rotation poses")
    if s.get("maxOccupiedSpriteTilesPerPose",0)<=0: errors.append("maxOccupiedSpriteTilesPerPose must be positive")
    if s.get("classificationOccupiedOnly") not in {"GOOD","WATCH","MAX","CONFLICT"}:
        errors.append("classificationOccupiedOnly must be known")
    reuse=d.get("primitiveReuseAssessment",{})
    if reuse.get("canRepeatSpritesForLongStraightStretches") is not True:
        errors.append("must assess repeated long-stretch sprites")
    if "edge-per-sprite" not in reuse.get("whyNotOneSpritePerCubeEdge",""):
        errors.append("must explain why edge-per-sprite is not starting model")
    poses=d.get("poses",[])
    if len(poses)!=4: errors.append("poses must contain four entries")
    for pose in poses:
        if len(pose.get("occupiedCells",[]))!=4:
            errors.append(f"{pose.get('stateId')} must use four P04_L cells")
        tiles=pose.get("spriteTileCoverage",{})
        if tiles.get("occupiedTileCount",0)<=0:
            errors.append(f"{pose.get('stateId')} must touch sprite tiles")
        if pose.get("estimatedSpriteBytesOccupiedOnly",0)!=tiles.get("occupiedTileCount",0)*64:
            errors.append(f"{pose.get('stateId')} sprite byte estimate mismatch")
if errors:
    print("ERROR: P04_L sprite feasibility report verification failed.")
    for e in errors: print(f"- {e}")
    raise SystemExit(1)
print("OK: P04_L sprite feasibility report verified.")
