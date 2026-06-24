# Card 030 — Capture Back macOS review surface generated image

## Status

Proposed / ready for Capture Back.

## Claim

The template Workbench should preserve the accepted generated infographic for the macOS Capture Back review-surface workflow.

## Decision

Add the approved image asset:

```text
assets/visuals/capture_back_macos_review_surface/capture_back_on_macos_review_surface.jpeg
```

and update the visual package README and visual spec to point to it as the current accepted infographic.

## Why this matters

The prior Capture Back established the operating procedure and preserved a source reference image. This Capture Back adds the actual generated image that expresses the current rule:

> Download to Downloads. Apply from repo root. Paste stdout back to chat. Review opened files. Commit only after approval.

The image makes the protocol teachable.

## What the image shows

The infographic presents:

- one chat with two roles: Workbench and II;
- the overlay download step into `~/Downloads`;
- terminal apply from the repo root;
- `unzip`, apply script, `make verify`, `make pack`, and `git status --short`;
- the step to paste Terminal stdout back into chat;
- the human review gate;
- commit only after approval;
- Workbench memory and history re-entry.

## Review standard

The image should be treated as an accepted generated asset. Future revisions may improve the visual, but this version establishes the template's current teaching asset.

## Related files

- `assets/visuals/capture_back_macos_review_surface/capture_back_on_macos_review_surface.jpeg`
- `assets/visuals/capture_back_macos_review_surface/README.md`
- `docs/visuals/capture_back_macos_review_surface_workflow.md`
- `CAPTURE_BACK_MACOS_REVIEW_SURFACE_IMAGE_ASSET.md`
