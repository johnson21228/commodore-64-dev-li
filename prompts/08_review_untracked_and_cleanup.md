# Review Untracked and Cleanup

Help review untracked files and likely overlay cruft in this Workbench LI repo.

Ask for or inspect:

```bash
git status --short
find . -maxdepth 3 -name '*overlay*' -o -name '__MACOSX' -o -name '.DS_Store'
```

Classify items as:

- should commit
- should delete
- generated/local only
- uncertain

Do not recommend deleting source material without clear evidence.
