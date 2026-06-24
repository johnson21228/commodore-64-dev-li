# C64 Lab Artifact Contract

A C64 Learning Lab card is complete when it produces a small, reviewable unit of learning.

## Required files for a lab

Each numbered lab should live under `labs/NNN_name/` and include:

```text
README.md
expected.md
src/
Makefile or documented build command
```

If a lab cannot be built yet because a local toolchain is not installed, the lab may remain in planned state, but the README must say so explicitly.

## Required explanation

Each lab README should identify:

```text
machine concept
what the program demonstrates
how to build it
how to run it in VICE
what the user should observe
what counts as evidence
```

## Evidence boundary

Generated files are evidence, not authority. A `.prg`, `.d64`, screenshot, or terminal log can be cited by a Capture Back, but the governing claims live in LI, docs, source maps, and captures.

## Progression rule

Prefer additive labs. A later lab may reuse ideas from an earlier lab, but it should not silently depend on hidden setup.

## First milestone definition

Milestone 1 is complete when the Workbench has:

```text
C64 Learning Lab project setup doc
Lab Artifact Contract
Lab sequence
First three lab folders
Verifier for lab completeness
VICE review workflow
Capture Back for the learning-lab direction
```
