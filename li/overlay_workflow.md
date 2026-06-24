# Overlay Workflow

The overlay workflow moves durable residue from chat reasoning into the repository.

A good overlay is:

- narrow
- explicit about files changed
- easy to apply from Terminal
- easy to review with git
- validated by local commands
- packed for sharing or later review

Canonical command shape:

```bash
cd /Users/stevejohnson/Developer/<repo>
unzip -o ~/Downloads/<overlay>.zip -d /Users/stevejohnson/Developer/<repo>
python3 apply_<overlay>.py
make verify
make pack
git status
```
