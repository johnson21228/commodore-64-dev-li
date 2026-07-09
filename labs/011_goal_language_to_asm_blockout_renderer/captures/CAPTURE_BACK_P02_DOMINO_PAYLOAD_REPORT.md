# Capture Back: P02_DOMINO Payload Report

## Decision

Begin the active-piece payload pipeline with a report-only target:

```text
P02_DOMINO
rotations: x_axis, y_axis
all legal x/y/z
no z_axis yet
no runtime drawing yet
```

This is not a database and not the final binary payload. It is the first decision instrument in the source-to-payload pipeline.

## Why this goes into the repo

The report belongs in the repo because it is generated evidence that governs the next engineering step.

It documents:

- the exact payload scope;
- the pose count;
- the estimated byte pressure;
- the decision classification;
- the manifest shape for future binary payloads.

This makes memory strategy reviewable instead of conversational.

## Generated artifacts

```text
dist/pieces/P02_DOMINO.payload_report.json
dist/pieces_manifest.json
```

The report is readable JSON. The future C64-loadable payload will be a compact binary file, but that is intentionally not part of this step.

## Decision role

The report answers:

- can one active piece family plausibly fit in the active payload slot?
- are byte/mask records too large?
- should we proceed to binary payload scaffolding?
- do we need compression, page loading, or a different representation?

## Current scope

The first report deliberately excludes `z_axis`.

That keeps the first measurement focused on:

- x/y movement;
- z-depth projection changes;
- in-place x/y rotation swap;
- one-current-payload discipline.

## Pipeline position

```text
piece source + pose rules
        ↓
P02_DOMINO payload report
        ↓
memory decision
        ↓
future binary payload
        ↓
future runtime loader/draw loop
```
