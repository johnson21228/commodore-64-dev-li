# Capture Back: Current-State Anti-Drift Rule

Capture this rule into the target Workbench.

## Observed failure mode

An LLM can drift when it reasons from inferred file shapes, stale context, or prior assumptions instead of the current repo or pack.

## Required correction

Steps 3, 4, and 5 of the Workbench LI loop must explicitly require current-state grounding.

## Rule text

```text
No Capture Back without current state.
```

## Operational meaning

Before Capture Back:

- inspect the current target repo, pack, status, or files
- do not patch from memory
- do not infer file shape when the current file can be inspected

During Verify:

- run the local checks
- confirm the change fits the current state
- confirm intended files only were touched

After Commit + Repack:

- the verified pack becomes the next reasoning baseline
- future reasoning starts from that current state
