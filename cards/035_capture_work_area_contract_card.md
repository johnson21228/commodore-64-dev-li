# Card 035 — Capture Work Area Contract

## Claim

The Workbench template needs a standard place for huge inputs, generated runs, databases, logs, and private archives that should not be included in the default II session pack.

## Decision

Adopt the Workbench Work Area Contract:

- `source/` is curated source authority.
- `examples/` and `fixtures/` are small representative material.
- `work/inputs/`, `work/runs/`, and `work/scratch/` are local working areas outside default Workbench governance.
- `private-artifacts/` is ignored/private archive space.
- `make pack` should produce the intentional II-consumable session pack, not a full archive.

## Durable rule

```text
Bulk work products are not Workbench memory until summarized, selected, and captured back.
```

## Capture Back result

Added:

- `docs/workbench_work_area_contract.md`
- `li/repo/work_area_contract.md`
- `notes/work_area_contract_lesson.md`
- `.gitignore` exclusions for standard bulk/private working areas
