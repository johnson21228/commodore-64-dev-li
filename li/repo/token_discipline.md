# Token Discipline

## Purpose

This LI keeps Workbench collaboration practical with LLM reasoning models.

## Rule

Use the smallest sufficient context.

## Preferred context order

1. Latest repo-history artifact for brief interpretation.
2. Specific files or snippets for focused edits.
3. Latest pack zip for broader repo reasoning.
4. Full repo only when pack/history is insufficient.

## Pack role

The pack is compacted repo context. It should contain enough LI, prompts, tools, cards, and evidence for an LLM to reason without the local repo.

## Anti-patterns

Avoid:

- pasting huge terminal logs when only the error matters
- uploading stale packs
- asking the LLM to infer repo state from memory
- treating old chat context as current authority
