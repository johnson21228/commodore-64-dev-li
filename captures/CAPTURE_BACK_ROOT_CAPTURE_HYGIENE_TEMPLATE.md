# Capture Back: Root Capture Hygiene Template Rule

## Summary

The Workbench Registry dashboard work revealed a reusable repo hygiene rule:

Root is the entry surface.
Capture Back records belong under `captures/`.

During rapid Capture Back work, many `CAPTURE_BACK_*.md` files can accumulate at repo root. That is useful during active work but weakens the repo as a clear entry point for humans and inference interfaces.

## Decision

The Workbench template now includes:

    captures/

as the standard durable location for Capture Back records.

## Rule

Future Workbench repos should place Capture Back records here:

    captures/CAPTURE_BACK_*.md

not at repo root.

## Root Boundary

The root of a Workbench LI repo should remain focused on:

    README.md
    SPINE.md
    MAP.md
    LLM_READ_FIRST.md
    HOW_LI_RULES.md
    Makefile

and other explicit entry/governance files.

## Template Effect

New Workbenches created from this template inherit `captures/.gitkeep`.

Capture Back prompts and overlay workflows should write durable CB records into `captures/`.
