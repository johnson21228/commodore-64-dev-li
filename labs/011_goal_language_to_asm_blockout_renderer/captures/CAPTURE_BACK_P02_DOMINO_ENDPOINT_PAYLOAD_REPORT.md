# Capture Back: P02_DOMINO Endpoint Payload Report

## Decision

The raw byte/mask report classified the first dynamic block payload as `CONFLICT`.

The next report measures a more memory-appropriate representation:

```text
P02_DOMINO
x_axis + y_axis
all legal x/y/z
projected endpoint segments
grid-reference estimate
no z_axis
no runtime drawing yet
no binary payload yet
```

## Rendering implication

Dynamic white outlined blocks should not begin with full per-pose raster byte/mask payloads.

The next viable direction is:

```text
prepared payload:
  projected line endpoints or compact grid references

runtime:
  generic line drawing
  dirty bounding restore/update
```

This still respects LI++ because the runtime does not reason about Blockout. It only executes prepared drawing records.

## Why this report exists

The report compares three directions:

```text
raw byte/mask records:
  fastest runtime, too much memory

endpoint segments:
  moderate memory, runtime line drawing

grid references:
  smaller payload, runtime endpoint lookup + line drawing
```

The report is a decision instrument before C64 runtime drawing or file I/O work.
