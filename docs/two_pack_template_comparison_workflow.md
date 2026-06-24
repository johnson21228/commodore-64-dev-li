# Two-Pack Template Comparison Workflow

## Purpose

This workflow helps compare any target Workbench pack against the current generalized Workbench template pack.

It answers two questions:

1. What current template improvements should move into the target Workbench?
2. What target Workbench structure, LI, prompts, or workflow patterns might be worth generalizing back into the template?

## Required inputs

Upload two packs:

1. Current template Workbench pack.
2. Target Workbench pack.

If possible, both packs should be generated after running:

```bash
make pack
```

This ensures the pack includes the latest generated history under:

```text
outputs/history/repo_history_for_llm_*.md
```

## Source of truth

The uploaded packs are the source of truth.

The assistant should inspect the latest history files first when present.

Conversation memory is not enough.

## Report outputs

The comparison should produce:

- packs inspected;
- latest history files found;
- executive summary;
- Template → Target sync candidates;
- Target → Template harvest candidates;
- already aligned items;
- do-not-move / target-specific items;
- recommended Template → Target overlay plan;
- possible Target → Template harvest plan;
- questions before applying;
- suggested next command or Capture Back request.

## Template → Target

This section finds what the target is missing from the current template.

Examples:

- review-surfaced Capture Back;
- macOS terminal Capture Back procedure;
- Start-Today Workbench guide;
- prompt to request WB Capture Back history;
- current-state anti-drift;
- generated asset handling;
- apply-script review summaries.

## Target → Template

This section finds target-specific improvements that may be generalized.

Examples:

- better prompts;
- clearer source maps;
- reusable LI rules;
- better cards;
- stronger asset structure;
- better domain-to-general pattern;
- improved onboarding or verification.

## Do not blindly copy

Domain-specific content should remain in the target unless generalized.

A good comparison distinguishes:

- directly reusable;
- reusable after generalization;
- target-specific only;
- do not move.

## Recommended next step

After the report, the user may ask for an overlay.

Do not generate the overlay before the user approves a plan.
