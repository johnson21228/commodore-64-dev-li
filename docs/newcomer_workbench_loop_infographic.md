# Newcomer Workbench Loop Infographic

This repo preserves prompts for generating newcomer-facing Workbench Loop infographics.

The default starter does not track generated infographic image assets.

Use these prompts when an image is needed:

```text
prompts/generate_newcomer_workbench_loop_infographic.md
prompts/generate_newcomer_multi_pack_workbench_loop_infographic.md
```

Generated images should be treated as drafts until a human explicitly selects one as a repo asset.

If an infographic is later added to the repo, add it through a separate explicit asset-add step with a validation note explaining why that image is good enough to become durable documentation.

## Current-state anti-drift rule

```text
No Capture Back without current state.
```

Steps 3, 4, and 5 must force current-state grounding:

- Capture Back must inspect the current target Workbench state before patching.
- Verify must prove the change fits the current state and does not drift.
- Commit + Repack must make the verified state the next reasoning baseline.

Short form:

```text
Reason from the current Workbench.
Capture Back into the current Workbench.
Verify before the Workbench remembers.
```
