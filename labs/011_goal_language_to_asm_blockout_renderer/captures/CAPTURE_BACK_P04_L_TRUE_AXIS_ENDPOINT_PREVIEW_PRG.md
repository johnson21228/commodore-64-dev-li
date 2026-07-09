# Capture Back: P04_L True-Axis Endpoint Preview PRG

## Decision

Build the first PRG using compact endpoint payloads instead of full bitmap-record payloads.

## Contract

```text
A/Q:
  rotate about x

S/W:
  rotate about y

D/E:
  rotate about z
```

## Runtime

```text
C64:
  reads key
  looks up next orientation
  clears bitmap
  draws sparse green wall/opening dots
  draws active block by runtime endpoint line drawing
```

## Why this matters

The full-bitmap true-axis preview was 43,695 bytes and failed.

The endpoint payload report estimated 3,736 bytes and classified as PATCH.

This PRG proves the compact-payload path.
