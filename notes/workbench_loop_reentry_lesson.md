# Capture Back: Workbench Loop Re-entry Lesson

This note captures a recurring Workbench failure mode: returning to a loop after interruption.

The danger is not the interruption itself. The danger is re-entering without re-anchoring and then mixing:

- intended Workbench-support changes
- product/runtime edits
- generated artifacts
- overlay/apply residue
- stale assumptions about what already ran

The fix is a named re-entry protocol.

A Workbench must support the human in saying:

```text
I am back. What loop was I in? What belongs in this commit? What must not be mixed?
```

The protocol preserves the Workbench promise: durable continuity, human custody, and small verified steps.
