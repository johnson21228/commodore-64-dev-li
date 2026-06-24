# Generated Artifacts Are Evidence

## Rule

Generated artifacts are evidence only. They do not govern the Workbench.

## Examples

Generated artifacts include:

- packs under `dist/`
- repo-history files under `outputs/history/`
- generated diagrams
- generated summaries
- generated reports
- exported PDFs, slides, HTML, or images

## Consequence

If a generated artifact is wrong, stale, or inconsistent, repair the governing LI, source, prompt, generator, test, verifier, or Makefile target that produced it.

Then regenerate the artifact.

## Why this matters

Without this boundary, a Workbench becomes a pile of stale outputs.

With this boundary, the repo remains governable.
