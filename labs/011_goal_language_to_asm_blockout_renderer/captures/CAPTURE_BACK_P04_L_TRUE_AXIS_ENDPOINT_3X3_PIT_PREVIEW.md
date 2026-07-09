# Capture Back: P04_L True-Axis Endpoint 3x3 Pit Preview

## Decision

Switch the endpoint preview to a 3x3x10 pit and restore more green pit reference points.

## Contract

```text
pit:
  3x3 cells
  10 deep
  more single-pixel green side-wall/opening dots
  no interior floor dots

active block:
  P04_L
  true x/y/z orientation table
  endpoint runtime line drawing
```

## Controls

```text
A/Q:
  rotate about x

S/W:
  rotate about y

D/E:
  rotate about z
```

## Why

The first endpoint PRG proved the compact payload path, but the pit was too sparse to read.

This version reduces the pit footprint to 3x3x10 and uses the projection system to generate many more green wall/opening dots.
