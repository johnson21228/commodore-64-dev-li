# Capture Back: Work Area Contract

## Decision

The Workbench template now distinguishes durable Workbench governance from bulk working material.

The default Workbench session pack is for II-consumable governance and selected evidence. It is not a full archive of all raw data, generated runs, logs, databases, private exports, or scratch work.

## Rule

```text
source/ may govern the Workbench.
work/ may inform the Workbench.
Only curated conclusions from work/ become durable Workbench memory.
```

## Standard folders

- `source/` — curated source material that can govern the Workbench.
- `examples/` — small representative examples safe for session packs.
- `fixtures/` — small test fixtures safe for verification and tests.
- `work/inputs/` — large raw imports, exports, datasets, and non-curated inputs.
- `work/runs/` — generated pipeline runs, logs, reports, derived outputs, and databases.
- `work/scratch/` — temporary experiments and intermediate material.
- `private-artifacts/` — full archives, private exports, big binaries, and material that should not enter ordinary II sessions.
- `dist/` — generated pack output.

## Pack consequence

`make pack` should create the small intentional Workbench session pack. It should exclude `work/`, `private-artifacts/`, nested zip files, databases, and other bulk/generated material unless a repo-specific contract explicitly allows a small representative fixture.

## Why

A Workbench is not strengthened by giving an II every byte. It is strengthened by giving the II the right boundary, source authority, cards, LI, prompts, history, and selected evidence.
