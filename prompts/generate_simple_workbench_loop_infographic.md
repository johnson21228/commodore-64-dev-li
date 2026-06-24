# Generate Simple Workbench Loop Infographic

You are generating a simple high-level infographic for a Workbench LI starter/template.

## Governing LI

Read first:

```text
li/workflow/high_level_workbench_loop.md
```

Also consult, but do not over-copy detail from:

```text
li/workflow/workbench_build_loop.md
li/repo/fresh_terminal_apply_command.md
```

## Required visual structure

Create a simple loop with five actions:

```text
1. Start with the Pack
2. Reason with the Model
3. Capture Back
4. Apply and Verify Locally
5. Commit and Repack
```

The loop should make clear that the updated pack starts the next cycle.

## Required message

Make these ideas visible:

- The Workbench is a git repo of LI.
- The pack is the portable context.
- The LLM helps reason.
- Capture Back moves useful reasoning, decisions, context, and continuity into the repo.
- Local verification and commit make continuity durable.
- The next pack carries continuity forward.

## Style guidance

Keep it simple.

Prefer fewer words over many labels.

Use one central loop.

Avoid detailed artifact lists.

Avoid listing every tool, prompt, directory, or Makefile target.

This is the first-impression infographic. The detailed workflow infographic can carry operational detail.

## Preferred default output

Create or update:

```text
docs/workbench_loop_simple_infographic.md
```

Use Mermaid unless the user asks for PNG, SVG, PDF, slides, or HTML.
