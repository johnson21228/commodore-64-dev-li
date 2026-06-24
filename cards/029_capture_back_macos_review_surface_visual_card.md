# Card 029 — Capture Back macOS review surface visual

## Status

Proposed / ready for Capture Back.

## Claim

The template Workbench should include a practical visual and operating guide for the current macOS Capture Back protocol.

The existing Stage 0 / original workflow infographic usefully shows one chat playing both Workbench and II roles while Terminal executes the durable repo update. The template should preserve that visual pattern, but reframe it as the current Capture Back review-surface workflow rather than as customer-facing stage language.

## Decision

Add a Capture Back macOS review-surface visual package to the template.

The package should explain:

- chat identifies what should be preserved;
- chat generates a Capture Back overlay zip;
- the human downloads the overlay to `~/Downloads`;
- Terminal applies the overlay from the repo root;
- verification and pack are run;
- key review files open;
- Terminal stdout is pasted back into chat for diagnosis;
- the human commits only after review;
- repo history enables future Workbench CB re-entry.

## Why this matters

The human operating protocol is part of Workbench.

The current macOS pattern depends on the relationship between:

- ChatGPT download behavior;
- the `~/Downloads` folder;
- Terminal commands;
- local repo root;
- apply scripts;
- verification and pack;
- raw stdout pasted back into chat;
- human review and commit;
- generated repo history.

Capturing this in the template makes future Workbenches easier to operate and easier to teach.

## Review standard

A future user should be able to open the visual package and understand:

1. why the overlay must be downloaded to Downloads;
2. why the command must be run from the repo root;
3. why stdout should be pasted back into chat;
4. why commit remains a human approval step;
5. how WB CB history is regenerated and used for re-entry.

## Related files

- `docs/capture_back_macos_terminal_procedure.md`
- `docs/visuals/capture_back_macos_review_surface_workflow.md`
- `li/repo/capture_back_macos_terminal_protocol.md`
- `assets/visuals/capture_back_macos_review_surface/README.md`
- `assets/visuals/capture_back_macos_review_surface/source_stage0_original_workflow_reference.jpeg`
- `prompts/capture_back_macos_terminal_apply_and_review.md`
- `prompts/request_workbench_cb_history.md`
- `notes/capture_back_download_terminal_history_lesson.md`
