# LI: Work Area Contract

## Principle

Bulk work products are not Workbench memory until summarized, selected, and captured back.

## Authority boundary

- `source/` may contain curated source authority.
- `examples/` and `fixtures/` may contain small representative material suitable for a session pack.
- `work/` is local working material by default.
- `private-artifacts/` is private/archive material by default.
- `dist/` is generated output.

## Default rule

The default `make pack` target must produce an II-consumable Workbench session pack, not a full repo archive.

It should exclude bulk, generated, private, and nested archive material unless a repo-specific contract explicitly allows a small representative fixture.

## Re-entry rule

If material in `work/` influences a decision, the decision must be captured back into durable Workbench form before it becomes shared Workbench memory.
