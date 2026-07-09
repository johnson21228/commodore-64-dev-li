# Capture Back: P03_ELBOW True-Axis Endpoint 3x3 Green-Line Pit Preview

## Decision

Begin the 3x3x10 pit with a three-cube L block, not the four-cube long L.

```text
piece:
  P03_ELBOW

canonical cubes:
  (0,0,0), (1,0,0), (0,1,0)

maximum footprint width:
  2
```

## Rendering

```text
pit:
  green projected grid lines
  3x3 cells
  10 deep
  no interior floor grid

active block:
  white endpoint-drawn outline
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

The 3-cube L fits the 3x3 pit better and gives an asymmetric shape for true x/y/z rotation without the long 3-wide footprint of `P04_L`.
