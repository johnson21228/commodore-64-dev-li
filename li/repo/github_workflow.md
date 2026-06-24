# GitHub Workflow

## Purpose

This LI defines how Workbench continuity may interact with GitHub.

## Rule

GitHub is a collaboration surface, not the Workbench's native unit of continuity.

The native workflow is the Workbench loop: Pack → Reason → Overlay → Verify → Commit + Repack.

## Recommended flow

1. Work locally with the Workbench repo.
2. Use LLM reasoning to generate overlays.
3. Apply, verify, pack, and commit locally.
4. Push commits to the remote.
5. Use GitHub for sharing, review, branches, pull requests, and access control.
6. Use optional continuity notes only when commit history and repo history are not enough.

## GitHub Issues

GitHub Issues may be used as containers.

They should not replace the repo's LI, history, verification, commits, and packs as the continuity record.
