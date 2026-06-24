# Capture Back Download, Terminal, and History Lesson

## Lesson

The current macOS Capture Back workflow depends on a concrete human protocol.

The assistant can generate the overlay, but the durable update happens through the user's local Terminal and repo.

## Captured insight

The protocol should be taught explicitly:

- download the overlay zip to `~/Downloads`;
- run the command from the Workbench repo root;
- unzip into the repo;
- run the apply script;
- verify and pack;
- inspect `git status --short`;
- open the key review files;
- paste stdout back into chat;
- let chat diagnose errors;
- commit only after review;
- use repo history for future re-entry.

## Why this matters

Workbench trust depends on visible custody.

The user should know where the zip goes, why the command works, what the terminal output proves, and where the history comes from.

## Product implication

The template Workbench should include both:

1. a review-surface rule; and
2. a practical macOS terminal procedure.

Together they make Capture Back teachable, auditable, and repeatable.

## One-line formulation

Download to Downloads. Apply from repo root. Paste stdout back to chat. Review opened files. Commit only after approval.
