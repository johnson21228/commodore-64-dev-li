# Capture Back: P04_L True Axis Above-Pit Preview

## Decision

Remove the z-only shortcut.

The preview now uses a real axis-specific orientation transition table:

```text
A/Q: rotate about x
S/W: rotate about y
D/E: rotate about z
```

The C64 runtime does not compute rotations. Workbench generates:

```text
orientationId + key -> nextOrientationId
```

The runtime only performs the table lookup and draws the prepared payload.

## Above-pit posture

The active block is placed at the pit opening/top plane, not on the floor.

```text
anchor: (1, 1, 0)
```

## Rendering posture

```text
pit:
  single-pixel green wall/opening dots only

floor:
  no dots

active block:
  white solid outline
```

Known artifact remains in hi-res bitmap mode:

```text
any green pit dot in a white active-block 8x8 cell becomes white
```

But the sparse wall-dot pit reduces the collision surface.
