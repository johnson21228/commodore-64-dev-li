# Infographic Prompt-Only Capture Back Gate

Workbench Loop infographics are useful newcomer-facing material, but generated image files are not captured back by default.

The default template captures back:

- prompts for generating newcomer Workbench Loop infographics
- LI that defines the desired concept, nomenclature, and quality bar
- docs that explain how to generate or select an infographic

The default template does **not** capture back generated bitmap/vector infographic assets as source truth.

## Rule

Generated infographic images are drafts until explicitly selected by a human.

Do not add or replace fixed infographic assets merely because an image was generated in chat.

A generated infographic image may be added only through an explicit asset-add step that records:

- why this image was selected
- where it will live in the repo
- whether it replaces an older asset
- how it was reviewed for readability, spelling, nomenclature, and layout quality

## Nomenclature guard

The visible loop step is **Capture Back**, not **Overlay**.

Use:

```text
Capture Back = the continuity act
Overlay = one possible technical delivery mechanism
Apply Command = the safe local execution path
```

## Quality guard

Generated infographics often degrade text, spacing, spelling, or conceptual emphasis.

Do not treat generated image output as canonical just because it is newer.

Prompts are durable guidance. Image assets require explicit human selection.
