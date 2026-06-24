# Card 026: Capture Root Capture Hygiene Template Rule

## Claim

Capture Back records should not accumulate at repo root.

## Decision

The Workbench template now includes `captures/` as the standard location for `CAPTURE_BACK_*.md` records.

## Rule

Root remains the entry surface. Capture evidence lives under `captures/`.

## Files

- `captures/.gitkeep`
- `captures/CAPTURE_BACK_ROOT_CAPTURE_HYGIENE_TEMPLATE.md`
- `docs/root_capture_hygiene.md`
- `li/repo/root_capture_hygiene_contract.md`
- `notes/root_capture_hygiene_template_lesson.md`
