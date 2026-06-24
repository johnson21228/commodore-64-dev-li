# Visible Workflow Outcome Contract

## Purpose

Every Workbench starter should include a visible explanation of the Workbench Build Loop.

The visible explanation helps a new human collaborator understand how the Workbench is used before they understand every LI file.

## Required visible outcome

A starter Workbench SHOULD generate or include a visible workflow artifact titled:

```text
Workbench Build Loop
```

The artifact SHOULD explain this loop:

```text
1. Add latest pack to chat
2. Prompt the model with the Workbench goal
3. Reason with the LLM
4. Capture Back into the repo with a downloadable change and terminal command
5. Run the command locally
6. Verify, test, pack, and commit
7. Use the updated pack for the next cycle
```

## Required audience

The visible workflow artifact should be understandable to:

- a non-technical domain owner
- a technical collaborator
- an LLM reasoning model
- a future reviewer of the repo

## Required message

The artifact MUST make these ideas visible:

- A Workbench is a git repo of LI.
- The pack is a zip file containing compacted Workbench context.
- The LLM reasoning model helps produce the next change.
- Capture Back transfers useful reasoning, decisions, context, and continuity from chat into the repo.
- Local verification and packing preserve continuity.
- The updated pack begins the next cycle.

## Acceptable formats

The visible outcome may be produced as:

- a Markdown diagram
- a Mermaid diagram
- an SVG
- a PNG
- a PDF
- a slide
- an HTML page

The starter SHOULD include a Markdown or Mermaid version by default because it is easy to diff, review, and regenerate.

## Authority

The visible workflow artifact is explanatory.

The governing authority remains this LI and the broader repository LI.
