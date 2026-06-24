# Pack and Share This Workbench

Help prepare this Workbench LI repo for sharing.

Check:

- README explains what the repo is
- SPINE names the purpose and boundary
- prompts are usable
- continuity cards are not empty placeholders only
- source material is intentionally included or intentionally omitted
- generated cruft is cleaned
- latest repo history artifact exists
- pack was generated

Recommended commands:

```bash
make verify
make pack
git status --short
ls -lh dist/
```

Then suggest a short message that explains how someone else should open and use the pack.
