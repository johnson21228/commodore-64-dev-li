# Existing Repo Conversion Protocol

## Claim

An existing repo can become a Workbench LI repo without being refactored into the template.

## Rule

When converting an existing repo pack into a Workbench, the assistant must:

1. inspect the uploaded pack as source authority;
2. identify the repo's existing purpose and structure;
3. preserve existing source, build, test, and product conventions;
4. add only the minimum Workbench LI layer needed for continuity;
5. produce an overlay-based Capture Back rather than a broad manual rewrite;
6. require human review before commit.

## Minimum viable Workbench layer

The initial layer should provide:

- read-first orientation;
- repo map;
- spine / thesis;
- LI rules;
- source authority model;
- continuity cards;
- history export;
- cleanup;
- verification;
- pack behavior;
- generated-artifact boundary.

## Anti-patterns

Do not:

- flatten the repo into the template;
- move product source unnecessarily;
- erase domain-specific structure;
- replace working build/test systems;
- treat generated outputs as governing truth;
- commit before human review.
