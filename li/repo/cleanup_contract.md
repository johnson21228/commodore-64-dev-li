# Cleanup Contract

## Purpose

This LI governs removal of transient files created by overlay and pack workflows.

## Cleanup should remove

- `overlay/`
- `apply_*_overlay.py`
- `.DS_Store`
- `__MACOSX/`
- stale generated history artifacts
- transient local output not intended for continuity

## Cleanup must not remove

- governing LI
- continuity cards
- source material
- prompts
- tools
- validation evidence intentionally preserved
- the latest useful history artifact

## Rule

Cleanup should make the repo easier to reason about without erasing continuity.
