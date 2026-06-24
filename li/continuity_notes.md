# Continuity Notes

## Purpose

Continuity notes are optional human-readable handoff notes.

They are not required for the Workbench loop.

## Rule

The primary Workbench loop is:

```text
Pack → Reason → Overlay → Verify → Commit + Repack → Repeat
```

A continuity note may be useful when a change needs extra explanation, but the loop does not depend on notes or cards.

## When to use a continuity note

Use a continuity note only when it helps preserve context that is not already clear from:

- the commit message
- the repo-history artifact
- the changed LI files
- terminal verification output
- the updated pack

## When not to use one

Do not create continuity notes just because a loop occurred.

Do not treat notes as the unit of work.

Do not make collaborators learn a card system before they can inspect or use the Workbench.

## Authority

Continuity notes are explanatory.

They do not outrank governing LI, source files, tests, verification output, commits, or human judgment.
