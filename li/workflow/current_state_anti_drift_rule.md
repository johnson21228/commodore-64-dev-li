# Current-State Anti-Drift Rule

Workbench LI must prevent reasoning drift.

The failure mode is simple:

```text
The model reasons from what it thinks is current.
The Workbench must force it to reason from what is actually current.
```

## Rule

No Capture Back without current state.

Before Capture Back, inspect the current target state.

During Verify, prove the change fits that state.

After Commit + Repack, use the new pack as the next reasoning baseline.

## Steps 3–5

### 3 — Capture Back

Capture back against the current target Workbench state.

Do not patch from memory, prior assumptions, stale packs, or inferred file shapes.

Inspect the current repo, pack, status, or target files first.

### 4 — Verify

Verify against the current state.

Run the local checks.

Confirm the patch touched the intended files only.

Confirm the reasoning, code, tests, docs, and capture-back record still agree.

### 5 — Commit + Repack

Commit only after verification passes.

Repack from the verified Workbench.

The new pack becomes the next reasoning baseline.

## Durable principle

```text
Reason from the current Workbench.
Capture Back into the current Workbench.
Verify before the Workbench remembers.
```
