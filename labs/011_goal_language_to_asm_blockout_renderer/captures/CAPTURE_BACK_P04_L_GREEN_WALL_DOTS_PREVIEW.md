# Capture Back: P04_L Green Wall-Dot Pit Preview

## Decision

Try the pit as green dots, with no floor dots:

```text
pit:
  green dots at projected side-wall/opening boundary intersections only

floor:
  no dots

active block:
  solid white outline
```

## Why

The screenshot showed the C64 hi-res bitmap 8x8 color-cell problem: when the active block needs a white foreground cell, any green pit pixels in that same cell also become white.

A dot-only, wall-only pit reduces pit pixels in active-block cells while preserving a spatial reference.

## Color strategy

```text
screen cells default:
  green foreground

active block touched screen cells:
  white foreground
```

Known artifact remains:

```text
a green pit dot in an active-block touched 8x8 cell will still become white
```

This preview tests whether sparse wall dots reduce the artifact enough.
