# High-Level Workbench Loop

## Purpose

This LI defines the highest-level Workbench loop for simple explanation and visual communication.

The detailed Workbench Build Loop remains useful for execution. This file governs the simplified version used for first impressions, overview graphics, collaborator orientation, and starter-template explanation.

## Governing idea

A Workbench grows by repeatedly capturing useful LLM-assisted reasoning back into a git-backed repo of Language Infrastructure.

## High-level loop

Use this five-part loop when explaining the Workbench at the highest level:

```text
1. Start with the Pack
2. Reason with the Model
3. Capture Back
4. Apply and Verify Locally
5. Commit and Repack
```

Then repeat with the updated pack.

## Plain-language version

### 1. Start with the Pack

The latest Workbench pack is added to chat.

The pack is a zip file containing compacted Workbench context.

### 2. Reason with the Model

The human and LLM reasoning model work together toward a specific Workbench goal.

The LLM supports reasoning. The human keeps judgment and custody.

### 3. Capture Back

When the reasoning is ready to become durable, the model helps create a downloadable repo change and an Apply Command.

Capture Back is the act of returning useful reasoning, decisions, context, evidence, and continuity from chat into the repo under human custody.

An overlay may be used as the technical delivery mechanism, but it is not the conceptual step in the Workbench Loop.

### 4. Apply and Verify Locally

The user opens a fresh terminal window, runs the Apply Command, and pastes the terminal output back into chat.

Verification, tests, cleanup, and pack generation provide evidence.

### 5. Commit and Repack

Accepted changes are committed to git.

A fresh pack is generated.

The new pack starts the next loop.

## Short form

```text
Pack → Reason → Capture Back → Verify → Commit + Repack → Repeat
```

## What must stay visible

Any high-level Workbench-loop explanation MUST show:

- the Workbench is a git repo of LI
- the pack carries repo context into chat
- the LLM is a reasoning partner, not the authority
- Capture Back transfers useful reasoning and continuity into the repo
- local verification and git commit make the work durable
- the updated pack begins the next cycle

## What to omit from a high-level infographic

A high-level infographic SHOULD omit most implementation detail.

Do not crowd the visual with:

- every artifact directory
- every prompt name
- every Makefile target
- all verification mechanics
- every intermediate file
- long explanatory prose

Those details belong in the detailed workflow artifact and governing LI.

## Relationship to detailed workflow

This file governs simple communication.

The detailed execution workflow remains governed by:

```text
li/workflow/workbench_build_loop.md
li/repo/overlay_workflow.md
li/repo/fresh_terminal_apply_command.md
li/repo/verification_contract.md
li/repo/packaging_contract.md
```

## Starter requirement

A mature starter SHOULD include both:

1. a detailed workflow explanation for operators
2. a high-level workflow explanation for first-time collaborators

## Current-state anti-drift rule

```text
No Capture Back without current state.
```

Steps 3, 4, and 5 must force current-state grounding:

- Capture Back must inspect the current target Workbench state before patching.
- Verify must prove the change fits the current state and does not drift.
- Commit + Repack must make the verified state the next reasoning baseline.

Short form:

```text
Reason from the current Workbench.
Capture Back into the current Workbench.
Verify before the Workbench remembers.
```
