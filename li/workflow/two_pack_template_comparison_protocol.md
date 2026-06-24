# Two-Pack Template Comparison Protocol

## Rule

When comparing a target Workbench against the generalized Workbench template, use a two-pack comparison.

The two inputs are:

1. the current template Workbench pack; and
2. the target Workbench pack.

The comparison should identify both:

- what should move from the template into the target; and
- what may be worth generalizing from the target back into the template.

## Source authority

Use the uploaded packs as source of truth.

Do not rely on conversation memory when pack contents or repo history are available.

If either pack contains:

```text
outputs/history/repo_history_for_llm_*.md
```

read the latest history file first.

Use history to understand recent Capture Backs, working-tree state, LI changes, docs, prompts, cards, notes, generated assets, and open decisions.

## Template → Target sync

Look for current generalized template capabilities missing or older in the target, including:

- Capture Back review surface rules;
- macOS Capture Back terminal workflow;
- download-to-Downloads convention;
- paste-terminal-stdout-back-to-chat loop;
- commit-after-review boundary;
- Start-Today Workbench prompt and protocol;
- WB Capture Back history request prompt;
- current-state anti-drift rules;
- repo history / re-entry protocol;
- generated asset handling rules;
- apply-script review summaries;
- open-file review surface behavior;
- newer generalized LI, docs, prompts, cards, notes, tools, or assets.

## Target → Template harvest

Look for target-specific patterns that may generalize, including:

- reusable workflow patterns;
- stronger prompts;
- improved LI;
- better Capture Back structure;
- source-map improvements;
- generated-asset handling improvements;
- onboarding improvements;
- verification or packaging improvements;
- review-surface improvements.

Do not copy domain-specific material into the template unless it can be generalized.

## Classification

Classify recommendations as:

1. directly reusable;
2. reusable after generalization;
3. target-specific only;
4. do not move.

## Implementation boundary

The comparison report should not generate an overlay unless explicitly requested.

First produce the report and a recommended plan.

## One-line principle

The template teaches the target, and the target may teach the template — but only through explicit comparison, review, and generalization.
