# Verification Contract

## Purpose

This LI defines what verification means for the starter/template.

## Minimum verification

A starter/template should verify that required files exist:

- read-first orientation
- map
- spine
- core LI
- workflow LI
- source/authority LI
- continuity-card LI
- prompts
- tools
- visible workflow artifact

## Verification is not proof of truth

Verification proves the repo satisfies expected structural checks.

It does not prove the Workbench's domain reasoning is correct.

## Required behavior

`make verify` SHOULD run both:

```text
tools/check_template_integrity.py
tools/verify_li_governance.py
```

## Rule

Do not claim the starter is ready unless verification passes or failures are explicitly reported.
