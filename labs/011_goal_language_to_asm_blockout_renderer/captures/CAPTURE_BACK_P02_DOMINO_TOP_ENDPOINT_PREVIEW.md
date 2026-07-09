# Capture Back: P02_DOMINO Top-Level Endpoint Preview

## Decision

Build the first visual proof from the endpoint/topology direction:

```text
P02_DOMINO
rotation: x_axis
pose: x=1, y=2, z=0
top level
white outlined dynamic block
pit visible as static base
preview only
```

## Scope

This is not active gameplay yet.

It does not add:

- movement;
- dirty restore;
- file I/O;
- runtime endpoint line drawing;
- lock/fill behavior.

It proves the visual target for the first dynamic white outlined block pose.

## Why this step exists

The endpoint report showed that full raster byte/mask payloads are too large.

This preview starts the next rendering path by showing the active block from endpoint/topology data on top of the pit.

## Color note

C64 hi-res bitmap color is cell-based. Cells touched by the active block use white foreground. This may turn any pit pixels in the same 8x8 cell white. That is acceptable for the first preview and should be revisited when the active overlay/restore path is implemented.
