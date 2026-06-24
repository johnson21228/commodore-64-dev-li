# Clean Pack Rebuild Contract

## Purpose

This LI requires Workbench packs to be rebuilt cleanly rather than updated in place.

## Rule

`make pack` SHOULD remove the existing pack zip before creating a new one.

This prevents stale files from remaining inside the zip after cleanup has removed them from the repo.

## Why

The `zip -r` command updates an existing archive. It does not automatically remove entries for files that no longer exist in the working tree.

Without a clean rebuild, stale history artifacts, old overlay files, or prior generated outputs may remain inside the pack even after cleanup succeeds.

## Required behavior

Before creating the pack, the pack command SHOULD run the equivalent of:

```bash
rm -f "$(PACK_PATH)"
```

Then it should create the zip from the current cleaned repo state.

## Validation expectation

A clean pack SHOULD contain:

- current governing LI
- current prompts and tools
- the latest useful repo-history artifact
- no stale history artifacts
- no overlay apply scripts
- no transient overlay directories
- no prior pack zip files
- no `.git` contents
- no `.DS_Store` files

## Authority

The clean pack is generated evidence.

The repo remains the continuity authority.
