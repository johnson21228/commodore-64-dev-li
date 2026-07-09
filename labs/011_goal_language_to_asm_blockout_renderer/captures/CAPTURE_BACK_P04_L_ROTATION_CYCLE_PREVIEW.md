# Capture Back: P04_L Four-State Rotation-Cycle Preview

## Decision

Switch the full-revolution visual proof from the symmetric domino to an existing L-shaped block.

Existing source piece:

```text
P04_L
canonicalCubes:
  [0,0,0]
  [1,0,0]
  [2,0,0]
  [0,1,0]
```

## Why

The domino is symmetric, so repeated rotations look like toggling.

P04_L is asymmetric, so repeated keypresses can visibly cycle:

```text
0 -> 90 -> 180 -> 270 -> 0
```

## Controls

ASAP preview controls:

```text
A/S/D -> advance one visible 90-degree step
Q/W/E -> reverse one visible 90-degree step
```

This is a visual full-revolution proof before generalized 3D axis rotation.

## Scope

Still preview-only:

- full-frame redraw;
- no dirty restore;
- no collision-aware legal rotation;
- no runtime line drawing;
- no file I/O.
