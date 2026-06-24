# Source Truth

## Purpose

This LI defines the source-of-truth order for a Workbench.

## Source truth order

1. Human/domain owner judgment.
2. Current repo source files and governing LI.
3. Git history.
4. Tests, verifiers, generators, and Makefile targets.
5. Continuity cards and source-context maps.
6. Generated history artifacts.
7. Packs and exports.
8. LLM interpretation.

## Rule

The repo is the continuity-bearing artifact.

An LLM may suggest changes. A human or team accepts changes by applying, reviewing, verifying, committing, and preserving them in the repo.
