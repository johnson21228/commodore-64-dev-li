# Visual — Start-Today Workbench Capture Back Guide

## Purpose

This visual specification defines the current best-practice infographic for explaining Start-Today Workbench.

## Title

Start-Today Workbench

## Subtitle

One chat window. Two roles. Local repo memory. Terminal-based Capture Back.

## Optional supporting line

This is the practical Stage 0 Workbench: useful before any dedicated app, MCP endpoint, or native product surface exists.

## Required visual zones

1. **ChatGPT Review Surface**
   - one chat window;
   - Workbench role;
   - II role;
   - accepted learning;
   - Capture Back proposal.

2. **Download Overlay**
   - overlay zip;
   - `~/Downloads`;
   - note that the command assumes the zip is there.

3. **Apply from Repo Root**
   - `cd /Users/.../<workbench-repo>`;
   - `unzip -o ~/Downloads/<overlay>.zip -d .`;
   - `python3 tools/<apply_script>.py`;
   - `make verify`;
   - `make pack`;
   - `git status --short`.

4. **Review Surface**
   - opened docs;
   - LI rules;
   - cards;
   - manifests;
   - generated assets.

5. **Paste stdout back to chat**
   - chat diagnoses from real repo evidence;
   - errors are repaired from facts;
   - commit command can be corrected.

6. **Human Commit Gate**
   - review first;
   - commit only after approval;
   - successful apply is not approval.

7. **Workbench Memory and Re-entry**
   - cards;
   - docs;
   - LI;
   - prompts;
   - notes;
   - assets;
   - `outputs/history/repo_history_for_llm_*.md`;
   - next chat starts smarter.

## Footer

Apply below. Review above. Commit only after human approval.

## Anti-drift rules

Do not make the visual look like a generic AI automation dashboard.

Do not imply the assistant commits automatically.

Do not hide the human review gate.

Do not make Stage 0 sound primitive or obsolete.

Do not use Stage 0 language for customer-facing solution pitches.

Make clear:

> Start-Today Workbench is already a real Workbench. It is the practical first surface before dedicated software.
