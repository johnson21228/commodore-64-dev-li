# Capture Back — Review Surface Rule

## Summary

This Capture Back adds a rule and reusable template for making overlay application reviewable.

It amplifies the emerging pattern where the apply script and apply command open the files that matter after the overlay is applied.

## Added

- `cards/028_capture_back_review_surface_rule_card.md`
- `li/repo/capture_back_review_surface_rule.md`
- `docs/capture_back_review_surface.md`
- `notes/capture_back_review_surface_lesson.md`
- `source/templates/capture_back_apply_script_template.py`
- `prompts/generate_capture_back_overlay_apply_command.md`
- `prompts/apply_overlay_terminal_workflow.md`
- `tools/apply_capture_back_review_surface_overlay.py`

## Navigation updated by apply script

- `MAP.md`
- `README.md`
- `WORKBENCH_REFERENCE.md`

## Review next

- `docs/capture_back_review_surface.md`
- `li/repo/capture_back_review_surface_rule.md`
- `source/templates/capture_back_apply_script_template.py`

## Intended behavior

Future Capture Back overlays should make the review path obvious:

> Apply below. Review above. Commit only after human approval.

## Suggested commit

```bash
git add MAP.md README.md WORKBENCH_REFERENCE.md \
  CAPTURE_BACK_REVIEW_SURFACE_RULE.md \
  cards/028_capture_back_review_surface_rule_card.md \
  li/repo/capture_back_review_surface_rule.md \
  docs/capture_back_review_surface.md \
  notes/capture_back_review_surface_lesson.md \
  source/templates/capture_back_apply_script_template.py \
  prompts/generate_capture_back_overlay_apply_command.md \
  prompts/apply_overlay_terminal_workflow.md \
  tools/apply_capture_back_review_surface_overlay.py

git commit -m "Capture review surface rule for overlays"
```
