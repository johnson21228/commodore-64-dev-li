# Authority Levels

## Purpose

This LI defines common authority labels for Workbench material.

## Levels

### Governing

Defines what should be true.

Examples: `SPINE.md`, `MAP.md`, `LLM_READ_FIRST.md`, core LI, workflow LI.

### Implemented

Defines what currently happens.

Examples: tools, Makefile targets, tests, scripts.

### Validating

Defines how claims are checked.

Examples: verifiers, tests, checklists, terminal output.

### Continuity-bearing

Preserves reasoning and handoff.

Examples: continuity cards, source-context maps, history artifacts.

### Generated evidence

Shows what was produced.

Examples: packs, generated reports, diagrams, exported files.

### Historical

Explains past decisions but may not govern current behavior.

Examples: old notes, archived prompts, prior pack summaries.

### Speculative

Useful thinking that has not yet been accepted.

Examples: brainstorms, rough notes, unreviewed LLM output.

## Rule

Do not use a lower authority level to override a higher authority level.
