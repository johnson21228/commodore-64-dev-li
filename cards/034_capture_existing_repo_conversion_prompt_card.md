# Card 034 — Capture existing repo conversion prompt

## Status

Proposed / ready for Capture Back.

## Claim

The template should include a clear prompt for transferring Workbench structure into an existing repo pack.

## Decision

Strengthen `prompts/convert_existing_repo_to_workbench_li.md` so it explicitly handles uploaded existing repo packs and asks for a narrow Workbench LI conversion rather than a broad refactor.

Add supporting workflow and LI files that distinguish two related operations:

1. converting a non-Workbench repo into a Workbench LI repo; and
2. comparing an already-Workbench target against the current template.

## Why this matters

Users often bring existing project repos, app repos, product repos, or client repos and ask whether Workbench can be added.

The template needs a prompt that protects the existing repo while still adding the governing Workbench layer: read-first files, map, spine, LI, cards, history, cleanup, verification, pack behavior, and Capture Back workflow.

## Related files

- `prompts/convert_existing_repo_to_workbench_li.md`
- `docs/existing_repo_conversion_workflow.md`
- `li/workflow/existing_repo_conversion_protocol.md`
- `prompts/README.md`
- `MAP.md`
- `CAPTURE_BACK_EXISTING_REPO_CONVERSION_PROMPT.md`
