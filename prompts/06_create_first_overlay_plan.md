# Create First Overlay Plan

Create a narrow overlay plan for improving this Workbench LI repo.

The overlay should be small, reviewable, and reversible.

Include:

- purpose of the overlay
- files to add or update
- files not to touch
- validation steps
- pack command
- git review command

Use this command shape when useful:

```bash
cd /Users/stevejohnson/Developer/<repo>
unzip -o ~/Downloads/<overlay>.zip -d /Users/stevejohnson/Developer/<repo>
python3 apply_<overlay>.py
make verify
make pack
git status
```

Do not perform broad refactors. Preserve source truth.
