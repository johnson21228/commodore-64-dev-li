# Packaging Contract

## Purpose

This LI defines what a Workbench pack is.

## Definition

A pack is a zip file containing compacted Workbench context for LLM reasoning and human sharing.

Canonical location:

```text
dist/<repo-name>.pack.zip
```

## Pack should include

- README and SPINE
- MAP and read-first LI
- core LI
- workflow LI
- source/authority LI
- optional continuity-note guidance
- prompts
- tools
- selected validation evidence
- latest useful repo-history artifact

## Pack should exclude

- `.git`
- prior packs
- cache files
- `.DS_Store`
- transient overlay directories
- local-only secrets
- large irrelevant binaries

## Rule

The pack is portable context, not the source of truth.

The repo remains authoritative.

## Commit order

If packs and history artifacts are tracked, Apply Commands should avoid running `make pack` after the final commit, because that can generate a new timestamped history artifact and dirty the working tree again.

See:

```text
li/repo/generated_artifact_commit_order.md
```
