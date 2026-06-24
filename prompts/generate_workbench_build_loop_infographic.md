# Generate Workbench Build Loop Infographic

You are helping maintain a Workbench LI starter/template repo.

Your task is to generate a visible infographic explaining the repeated Workbench Build Loop.

## Governing LI

Before generating the infographic, read:

```text
li/workflow/workbench_build_loop.md
li/workflow/visible_workflow_outcome_contract.md
```

## Required content

The infographic must show this loop:

```text
1. Current Workbench repo contains LI.
2. `make pack` compacts the LI into a zip pack.
3. The user adds the latest pack to a chat with an LLM reasoning model.
4. The user prompts the model with the Workbench goal.
5. The user and model reason together.
6. The user asks the model to Capture Back useful reasoning into a downloadable change and terminal command.
7. The user downloads the change and runs the terminal command locally.
8. The command applies changes, verifies/tests, packs, and prepares the repo for commit.
9. The updated pack starts the next cycle.
```

## Required message

Make these ideas obvious:

- The Workbench is the durable source of continuity.
- Chat is a reasoning surface, not the system of record.
- Capture Back is the bridge from reasoning back into the repo.
- Verification and commit make the change durable.
- The next pack carries continuity forward.

## Preferred default output

Create or update:

```text
docs/workbench_build_loop_infographic.md
```

Use Mermaid unless the user asks for SVG, PNG, PDF, slides, or HTML.

## Style

Use plain language.

Prefer a loop diagram over a linear checklist.

Do not overcomplicate the diagram.

Do not claim the LLM directly modifies the repo unless the actual workflow gives it repo access.
