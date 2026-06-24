# Team Member Onboarding Protocol

A Workbench should support onboarding a new collaborator without requiring them to understand every file first.

This protocol treats a newcomer as a clean-room reader who needs to understand:

```text
What is this?
Why does it exist?
How do I use it?
What do I touch first?
How do I avoid breaking the workflow?
How do I give useful feedback?
```

## Purpose

The goal is not to explain the entire repo.

The goal is to test whether the repo can help a smart new collaborator understand the Workbench promise and participate responsibly.

## Onboarding posture

A new team member should begin with read-only orientation.

They should first read:

```text
README.md
SPINE.md
LLM_READ_FIRST.md
MAP.md
docs/first_use.md
docs/what_to_upload_to_an_llm.md
```

Then they should produce a reaction note, not a code or repo change.

## First low-risk contribution

The safest first contribution is a short newcomer reaction note:

```text
notes/<person_or_role>_first_read_reaction.md
```

The note should answer:

1. What do you think this repo is for?
2. What part made sense immediately?
3. What part was confusing?
4. Where would you expect to start?
5. What would make you comfortable using this workbench?
6. What questions do you need answered before contributing?

## Simulation protocol

Before inviting a person, run a clean-room onboarding simulation with the repo pack.

The simulation should ask an LLM to act as a smart new team member with read-only access and report:

1. What the Workbench appears to be.
2. What problem it is trying to solve.
3. How the Workbench Loop works.
4. What Capture Back means.
5. The first files to read.
6. What not to touch or assume yet.
7. What is confusing.
8. What would make participation comfortable.
9. A first low-risk action.
10. Questions to ask the workbench owner.

## Guardrails

- Do not begin with broad editing.
- Do not ask the newcomer to understand every file.
- Do not treat GitHub Issues as the whole work unit.
- Preserve human custody: the team decides what gets captured back.
- Keep the first contribution small, inspectable, and reversible.
