# Workbench Work Area Contract

A Workbench repo may contain large local data, generated runs, imports, exports, scratch work, and private archives. That material should not be treated as ordinary Workbench governance and should not enter the default II session pack.

## The distinction

```text
Workbench governance
→ small, durable, II-consumable, versioned, and reviewable

Workbench working data
→ large, noisy, local/private, generated, reproducible, or temporary
```

## Standard folder convention

Use these folders consistently:

```text
source/                  curated source material that may govern the WB
examples/                small representative examples safe for session packs
fixtures/                small test fixtures safe for verify/tests
work/inputs/             huge raw imports, exports, datasets, and bulk inputs
work/runs/               generated pipeline runs, logs, reports, sqlite/db files
work/scratch/            temporary experiments and intermediate material
private-artifacts/       full archives, private exports, big binaries
dist/                    generated pack output
```

## Governing rule

```text
source/ may govern the Workbench.
work/ may inform the Workbench.
Only curated conclusions from work/ become durable Workbench memory.
```

## Default session-pack exclusions

A default Workbench session pack should exclude:

```text
work/inputs/**
work/runs/**
work/scratch/**
private-artifacts/**
dist/**
*.zip
**/*.zip
*.sqlite
**/*.sqlite
*.db
**/*.db
.DS_Store
__MACOSX/
```

Large `*.jsonl` files should usually be excluded unless they live in `examples/` or `fixtures/` and are intentionally small.

## Capture Back path

When a run or bulk input matters, do not pack the whole run by default. Capture the lesson back as one or more durable artifacts:

```text
notes/run_<date>_summary.md
docs/pipeline_observation.md
cards/00x_capture_pipeline_run_lesson.md
li/<domain>/selected_rule.md
```

## Product consequence

Registry, dashboard, and `WB_SESSION_REQUESTS` should consume the Workbench session pack, not a full private archive. Full archives may exist, but they belong in ignored/private storage and should require explicit human selection.
