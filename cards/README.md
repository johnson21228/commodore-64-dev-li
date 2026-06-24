# Cards Directory

This starter no longer treats cards as a required Workbench concept.

The primary Workbench loop is:

```text
Pack → Reason → Overlay → Verify → Commit + Repack → Repeat
```

Optional handoff notes may be kept under `notes/` when useful.

See:

```text
li/continuity_notes.md
```

## When to create a card

Cards are optional, but they become important when a Workbench Loop becomes a governed unit of work, not just an edit.

A good test:

> If this change would be confusing, risky, or incomplete when seen only as a git diff, make a card.

A card should capture:

- intent
- context
- decision
- execution
- evidence
- outcome
- next handoff

This is especially important for repo authority changes, migrations, deletions, cleanup, and work that splits across multiple commits.
