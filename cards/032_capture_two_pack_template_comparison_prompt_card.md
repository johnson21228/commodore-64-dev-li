# Card 032 — Capture two-pack template comparison prompt

## Status

Proposed / ready for Capture Back.

## Claim

The template Workbench should include a reusable prompt for comparing any target Workbench pack against the current template Workbench pack.

## Decision

Add a two-pack comparison prompt that asks the assistant to inspect:

1. the current generalized template WB pack; and
2. a target WB pack.

The prompt should produce:

- Template → Target sync candidates;
- Target → Template harvest candidates;
- already-aligned items;
- target-specific items that should not move;
- an overlay plan for syncing the target;
- possible future Capture Backs for improving the template.

## Why this matters

As the template evolves, existing Workbenches may lag behind.

A power user needs a repeatable way to ask:

- What current template improvements should move into this target Workbench?
- What does this target Workbench teach that may belong back in the generalized template?

This supports bidirectional learning without blind copying.

## Source authority

The uploaded packs are the source of truth.

If either pack includes:

```text
outputs/history/repo_history_for_llm_*.md
```

the latest history file should be read first.

## Review standard

The prompt should instruct the assistant to avoid blindly copying domain-specific material into the template.

Recommendations should be separated into:

1. directly reusable;
2. reusable after generalization;
3. target-specific only;
4. do not move.

## Related files

- `prompts/compare_target_workbench_against_template_pack.md`
- `docs/two_pack_template_comparison_workflow.md`
- `li/workflow/two_pack_template_comparison_protocol.md`
- `notes/two_pack_template_comparison_prompt_lesson.md`
