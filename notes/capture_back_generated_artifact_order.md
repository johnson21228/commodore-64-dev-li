# Capture Back Note: Generated Artifact Commit Order

## What happened

While creating the Workbench Consulting LI repo, the workflow verified and packed the repo after the initial commit.

`make pack` generated a new timestamped history artifact and rebuilt the pack. That made the working tree dirty again, requiring an extra generated-artifact commit.

## Lesson

A Workbench Apply Command must respect generated artifact commit order.

Do not run `make pack` after the final commit unless the command also commits the generated artifacts and stops.

## Captured back into template

This lesson is captured in:

```text
li/repo/generated_artifact_commit_order.md
prompts/apply_command_generated_artifact_order.md
```

## Updated preferred loop

```text
apply overlay
→ verify
→ pack
→ commit
→ status clean
```

Not:

```text
apply overlay
→ verify
→ commit
→ pack
→ dirty status
```
