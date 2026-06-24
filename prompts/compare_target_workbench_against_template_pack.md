# Prompt — Compare Target Workbench Against Current Template Pack

I am uploading two Workbench packs:

1. **Current Template WB pack**  
   This is the current generalized Workbench template and should be treated as the source of current template best practices.

2. **Target WB pack**  
   This is a specific Workbench repo that may need to be updated with template improvements.

Your job is to compare the two packs and produce a practical synchronization report.

## Important source authority

Use the uploaded packs as the source of truth.

Do not rely only on conversation memory.

If either pack contains:

```text
outputs/history/repo_history_for_llm_*.md
```

read the latest history file first.

Use the history files to understand recent Capture Backs, cards, LI changes, prompts, docs, generated assets, and open working-tree state.

## Goal A — Template → Target update candidates

Identify what should likely move **from the current template WB into the target WB**.

Look especially for newer generalized template capabilities such as:

- Capture Back review surface rules;
- macOS Capture Back terminal workflow;
- download-to-Downloads convention;
- paste-terminal-stdout-back-to-chat loop;
- human commit-after-review boundary;
- Start-Today Workbench / Stage 0 educational prompt;
- prompts for requesting WB Capture Back history;
- current-state anti-drift rules;
- repo history / re-entry protocols;
- generated asset handling rules;
- apply-script review summaries;
- open-file review surface behavior;
- any newer LI, docs, prompts, cards, notes, tools, or assets present in the template but missing in the target.

For each candidate, report:

```text
Template item:
Target status: missing / older / partially present / already present
Why it matters:
Recommended action:
Files likely involved:
Risk level:
```

## Goal B — Target → Template harvest candidates

Identify any structure, LI, prompts, docs, cards, notes, tools, or generated assets in the **target WB** that might be valuable to generalize back into the template.

Look for:

- reusable workflow patterns;
- better prompts;
- stronger LI rules;
- improved Capture Back patterns;
- useful source-map structures;
- better docs organization;
- better generated-asset handling;
- domain-specific patterns that could be generalized;
- verification or packaging improvements;
- onboarding improvements;
- review-surface improvements;
- any repeated pattern that seems useful beyond the target domain.

For each harvest candidate, report:

```text
Target item:
Why it may generalize:
What template gap it fills:
How to generalize it:
Files likely involved:
Risk level:
```

## Goal C — Do not blindly copy

Do not recommend copying domain-specific material into the template unless it can be generalized.

Separate recommendations into:

1. **Directly reusable**
2. **Reusable after generalization**
3. **Target-specific only**
4. **Do not move**

## Goal D — Produce an implementation plan

After the comparison, produce a practical implementation plan.

Include:

### Template → Target overlay plan

List files that should be added or updated in the target WB.

Prefer an overlay-based Capture Back plan, not manual edits.

Include a suggested overlay name:

```text
<target-name>-template-sync-overlay.zip
```

Include a suggested card name:

```text
cards/0XX_sync_current_template_improvements_card.md
```

Include a suggested commit message:

```text
Sync current Workbench template improvements
```

### Target → Template harvest plan

List possible future Capture Backs into the template.

Include:

- proposed card names;
- proposed LI/doc/prompt files;
- what should be generalized;
- what should not be copied.

## Goal E — Report format

Use this structure:

```text
# Workbench Template Comparison Report

## Packs inspected

- Template pack:
- Target pack:
- Latest template history:
- Latest target history:

## Executive summary

## Template → Target sync candidates

## Target → Template harvest candidates

## Already aligned

## Do not move / target-specific only

## Recommended next overlay: Template → Target

## Possible future overlay: Target → Template

## Questions before applying

## Suggested next command or Capture Back request
```

## Important behavior

If the target pack is missing current repo history, say so and ask for the latest:

```text
outputs/history/repo_history_for_llm_*.md
```

or a newer target pack.

If the template pack appears older than the target pack, say so and do not assume the template is authoritative.

If both packs include histories, compare by the content of the histories and files, not just timestamps.

Do not generate an overlay until I explicitly ask for it.

First produce the comparison report and recommended plan.
