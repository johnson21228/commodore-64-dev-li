# Visual — Capture Back on macOS Review Surface Workflow

## Purpose

This visual package preserves the current human-operable Capture Back workflow on macOS.

It is based on the earlier Stage 0 / original workflow visual pattern, but reframes the concept as a practical Capture Back review-surface protocol.

## Accepted generated infographic

The current accepted infographic is stored at:

```text
assets/visuals/capture_back_macos_review_surface/capture_back_on_macos_review_surface.jpeg
```

## Recommended title

Capture Back on macOS: From Chat Reasoning to Workbench Memory

## Recommended subtitle

Download to Downloads. Apply from repo root. Paste stdout back to chat. Review opened files. Commit only after approval.

## Source visual reference

The source reference image is stored at:

```text
assets/visuals/capture_back_macos_review_surface/source_stage0_original_workflow_reference.jpeg
```

That image usefully showed:

- one ChatGPT conversation playing both Workbench and II roles;
- Terminal executing the durable part of the loop;
- Workbench reviewing and approving what becomes durable.

## Required updated visual zones

A refined version should show these operational zones:

1. **Chat proposes what should be preserved**
   - decision;
   - rule;
   - prompt;
   - note;
   - generated artifact;
   - source evidence.

2. **Capture Back overlay is generated**
   - overlay zip;
   - apply script;
   - manifest;
   - review checklist.

3. **Human downloads to `~/Downloads`**
   - explain that the terminal command expects the zip there.

4. **Terminal applies from repo root**
   - `cd /Users/.../<repo>`;
   - `unzip -o ~/Downloads/<overlay>.zip -d .`;
   - `python3 tools/<apply_script>.py`.

5. **Verification and pack**
   - `make verify`;
   - `make pack`;
   - `git status --short`.

6. **Review surface opens**
   - primary doc;
   - LI rule;
   - generated artifact;
   - Capture Back manifest.

7. **Paste stdout back into chat**
   - chat diagnoses errors;
   - chat confirms expected status;
   - chat proposes repairs if needed.

8. **Human commits after review**
   - explicit `git add`;
   - explicit `git commit`;
   - final `git status --short`.

9. **History enables re-entry**
   - `outputs/history/repo_history_for_llm_*.md`;
   - future chat reads current state before making claims.

## One-sentence visual summary

Capture Back turns accepted chat learning into local Workbench memory: download the overlay, apply from repo root, verify, review opened files, paste stdout back to chat, then commit only after human approval.

## Anti-drift rules

Do not frame this as customer-facing stage language.

Do not make the visual look like generic automation or a black-box agent.

The visual should make human custody visible:

- human downloads;
- human runs Terminal;
- human reviews opened files;
- human pastes evidence back into chat;
- human commits after approval.

## Relationship to review-surface LI

This visual is the practical companion to the review surface rule:

> Apply below. Review above. Commit only after human approval.
