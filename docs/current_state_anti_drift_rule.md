# Current-State Anti-Drift Rule

This is the practical discipline behind the Workbench loop.

```text
The model reasons from what it thinks is current.
The Workbench must force it to reason from what is actually current.
```

## Loop correction

Step 3 — Capture Back:

```text
Capture back against the current target Workbench state.
Do not patch from memory, stale packs, prior assumptions, or inferred file shapes.
```

Step 4 — Verify:

```text
Verify against the current state.
Run local checks.
Confirm reasoning, code, tests, docs, and capture-back record agree.
```

Step 5 — Commit + Repack:

```text
Commit only after verification passes.
Repack from the verified Workbench.
Use the new pack as the next reasoning baseline.
```

## Short form

```text
Use the current context.
Update the right Workbench.
Verify before memory.
Keep building.
```
