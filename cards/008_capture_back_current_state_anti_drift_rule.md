# 008 — Capture Back: Current-State Anti-Drift Rule

## Observation

The Workbench loop can fail if the model reasons from stale assumptions instead of the current repo or pack.

This happened during the Take60 sensor-shutdown work: multiple overlays were generated from inferred test shapes before the current file state was inspected.

## Decision

The Workbench LI loop now requires current-state grounding in steps 3, 4, and 5.

## Rule

```text
No Capture Back without current state.
```

## Meaning

The model reasons. The Workbench remembers. But before the Workbench remembers, it must force the model to reason from what is actually current.

## Applies to

- Capture Back
- Verify
- Commit + Repack
- future overlay generation
- future repo patching
- future pack interpretation
