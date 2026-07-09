# Capture Back: P04_L Dot-Only Pit Preview

## Decision

Try a dot-only pit language:

```text
pit:
  dots at projected grid intersections

active block:
  solid white outline
```

## Why

Continuous pit lines compete with the active block in C64 hi-res bitmap mode.

The green/white version showed that changing an 8x8 cell foreground color for the active block also changes any pit pixels in that same cell.

A dot-only pit reduces the number of pit pixels that can collide with active-block cells.

## Scope

This preview remains bitmap-only and all-white. It tests whether the pit can still read as 3D space when represented by sparse projected grid intersections.

It does not yet solve:

- green pit plus white active block;
- sprite overlay;
- dirty restore;
- collision-aware rotation.
