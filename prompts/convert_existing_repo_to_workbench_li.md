# Convert Existing Repo Pack to Workbench LI

I am uploading an **existing repo pack** that is not yet a Workbench LI repo, or only partially follows the Workbench pattern.

Your job is to help transfer the current Workbench structure into that repo while preserving the repo's existing purpose.

## Source authority

Use the uploaded repo pack as the source of truth.

Do not rely on conversation memory.

If the uploaded pack contains:

```text
outputs/history/repo_history_for_llm_*.md
```

read the latest history file first.

If the pack does **not** contain repo history, inspect the file tree and the most important read-first files instead, such as:

```text
README.md
Makefile
package manifests
source folders
existing docs
existing prompts
existing tests
```

## Goal

Add the **minimum governing Workbench LI layer** needed to make the existing repo usable in the Workbench loop.

Do **not** do a broad refactor.

Do **not** rename, reorganize, or rewrite the existing product/project unless required for safety, verification, or pack behavior.

Preserve the repo's existing purpose, language, test system, and working conventions.

## Required Workbench structure to consider

Add or update only what is missing or clearly stale:

```text
LLM_READ_FIRST.md
MAP.md
HOW_LI_RULES.md
SPINE.md
li/core/
li/workflow/
li/repo/
li/source/
li/cards/
cards/
prompts/
tools/
outputs/history/.gitkeep
dist/.gitkeep
```

The target repo does not need to become a clone of the template. It needs enough structure to preserve continuity, decisions, source authority, validation evidence, and Capture Back behavior.

## Required behavior to add

The converted repo should support:

- read-first orientation for LLMs and humans;
- a map of governing files and source authority;
- core Workbench principles;
- source/context authority rules;
- continuity cards;
- Capture Back overlay workflow;
- history export for re-entry;
- cleanup of generated LI artifacts;
- verification checks;
- pack generation;
- generated artifacts as evidence only;
- human review before commit;
- terminal apply-and-review workflow on macOS when relevant.

## Existing repo respect rule

Before recommending files to add, identify:

```text
Repo purpose:
Existing build/test commands:
Existing package or app structure:
Existing docs/source authority:
Existing generated outputs:
Likely files that must not be disturbed:
```

Then propose the narrowest Workbench layer that fits.

## Output format

First produce a conversion report:

```text
# Existing Repo → Workbench LI Conversion Report

## Pack inspected

## Existing repo purpose

## Existing structure to preserve

## Missing Workbench layer

## Files to add or update

## Files not to touch

## Verification and pack commands

## Risks

## Recommended Capture Back overlay

## Suggested terminal apply command
```

## Overlay requirement

When asked to generate the update, produce a narrow Capture Back overlay, not a manual edit list.

Use a suggested overlay name like:

```text
<repo-name>-workbench-li-conversion-overlay.zip
```

Use a suggested card name like:

```text
cards/0XX_convert_existing_repo_to_workbench_li_card.md
```

Use a suggested commit message like:

```text
Add Workbench LI governance layer
```

## Review standard

The overlay should open review surfaces after applying, typically:

```text
open LLM_READ_FIRST.md
open MAP.md
open SPINE.md
open cards/0XX_convert_existing_repo_to_workbench_li_card.md
```

The user should commit only after review.
