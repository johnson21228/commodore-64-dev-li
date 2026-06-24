# Repo Worker Token Economy Brainstorm

## Status

Brainstorm / future LI candidate.

This is not yet an implementation patch. It captures a Workbench product idea for the Registry and Template.

## Trigger

The Workbench loop currently spends high-value II tokens on two different kinds of work:

1. Reasoning, judgment, durable LI decisions, and artifact generation.
2. Repetitive repository-operation loops: terminal command generation, paste-back interpretation, verifier triage, pack/status/commit sequencing.

The user identified that a local Ollama-backed repo worker could handle the second role without becoming the II.

## Captured Idea

Workbench should separate the II reasoning role from the RepoOps local worker role.

### II / Reasoning Role

The II remains responsible for:

- understanding user intent
- deciding what should become durable LI
- designing Capture Back changes
- generating artifacts
- resolving ambiguous product/workflow questions
- reviewing final evidence when needed

### RepoOps / Local Repo Worker Role

A local LLM, such as Ollama, may act as the repository worker for:

- generating pasteable terminal command blocks
- reading pasted terminal output
- interpreting `make verify`, `make pack`, and `git status`
- diagnosing failed verifiers
- proposing the next terminal command
- preparing compact evidence packets
- helping reach clean/verified/packed/committed repo state

The RepoOps worker is not the II. It is a local repository work layer.

## Token Economy Thesis

Workbench should reserve premium II context for reasoning, LI judgment, and artifact generation.

Routine repo-terminal work may be delegated to a local RepoOps worker so that II token use becomes a smaller share of total work-loop tokens.

Core metric:

```text
II Token Fraction = II tokens / (II tokens + RepoOps tokens)
```

or:

```text
Premium Reasoning Token Share = II / (II + RepoOps)
```

## Why This Matters

A large amount of Workbench token use is operational churn:

- paste terminal output
- inspect failure
- generate next command block
- run verifier
- paste output again
- run pack
- interpret git status
- stage and commit

This work is important, but it does not always require the high-value II reasoning layer.

A local RepoOps worker could absorb this loop and report back to the II with compact evidence.

## Example Evidence Packet

```text
REPO_WORKER_EVIDENCE

repo: wc2026-bracket-tracker-li
task: root Capture Back hygiene cleanup
status: PASS

actions:
- moved 11 root CAPTURE_BACK_*.md files into captures/
- left legacy capture_back/ records untouched
- ran clean_repo_hygiene
- ran make verify
- ran make pack
- committed locally

verification:
- make verify passed
- make pack passed
- working tree clean

git:
- branch ahead origin/main by 1 commit

token_use:
- ii_tokens: estimated or measured
- repo_ops_tokens: estimated or measured
- ii_token_fraction: II / (II + RepoOps)

human_decision_needed:
- push or continue locally
```

## Candidate Metrics

Workbench Registry could track:

```text
ii_tokens
repo_ops_tokens
total_loop_tokens
ii_token_fraction
repo_ops_token_fraction
ii_turn_count
repo_ops_turn_count
terminal_pasteback_bytes
commands_generated
commands_run
verify_runs
pack_runs
commits_created
human_approval_points
session_type
result
```

Session types may include:

```text
reasoning
artifact_generation
cb_authoring
repo_apply
verify_pack
repair_loop
commit_prep
```

The metric should be interpreted by session type.

For example:

- Low II fraction is good for routine repo-apply loops.
- Higher II fraction is expected for product reasoning or artifact generation.
- Low II fraction during ambiguous design work may be suspicious.

## Candidate Registry LI

Possible future file:

```text
li/workflow/local_repo_worker_token_economy.md
```

Candidate rule:

```text
Workbench should measure the split between II reasoning tokens and local RepoOps tokens. The core ratio is II / (II + RepoOps). This ratio helps evaluate whether premium II context is being reserved for reasoning, durable LI judgment, and artifact generation while local worker tokens absorb repetitive repo-terminal loops.
```

## Candidate Template LI

Possible future file:

```text
li/workflow/repo_worker_terminal_loop.md
```

Candidate rule:

```text
A Workbench may use a local repo worker LLM to generate terminal commands and interpret terminal paste-back during apply, verify, pack, status, and commit-prep loops. The repo worker is not the II and not the source of Workbench judgment. Its output is valid only when checked by repository verification, git status, and human approval at mutation, commit, and push boundaries.
```

## Candidate Registry Dashboard Surface

The registry dashboard could show:

```text
Repo                       II Share   RepoOps Share   Result
wc2026-bracket-tracker-li  16%        84%             PASS
workbench-registry-li      28%        72%             PASS
iam-watch-li               61%        39%             REVIEW
```

This would turn the Ollama/local-worker idea into a measurable Workbench product claim.

## Safety Boundary

The RepoOps worker may:

- generate terminal commands
- interpret terminal output
- summarize evidence
- classify pass/fail state
- suggest next command blocks

The RepoOps worker may not, by default:

- become the II
- invent durable LI
- decide product direction
- execute arbitrary commands without approval
- commit or push without explicit human approval
- override repo verification
- treat local model output as source of truth

## Proposed Next Step

Capture this as a brainstorm note in both Registry and Template, then later promote it into LI after one or two controlled experiments.

Future implementation could add:

```text
records/metrics/repo_worker_token_sessions.jsonl
tools/wb_repo_worker_metrics.py
docs/repo_worker_token_economy.md
```
