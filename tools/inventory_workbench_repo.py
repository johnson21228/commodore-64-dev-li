#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
OUT_DIR = ROOT / "artifacts"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUT = OUT_DIR / f"workbench_repo_inventory_{STAMP}.md"


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return e.output


def fence(text: str) -> str:
    return "```text\n" + text.rstrip() + "\n```\n"


def find_lines(args: list[str]) -> str:
    return run(args)


def section(title: str, body: str) -> str:
    return f"\n## {title}\n\n{body}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    branch = run(["git", "branch", "--show-current"]).strip()
    now = datetime.now().astimezone().strftime("%a %b %d %H:%M:%S %Z %Y")

    authority_files = []
    for name in [
        "LLM_READ_FIRST.md",
        "HOW_LI_RULES.md",
        "SPINE.md",
        "MAP.md",
        "README.md",
        "Makefile",
        ".gitignore",
    ]:
        if (ROOT / name).exists():
            authority_files.append(name)

    wb_dirs = []
    for d in ["LI", "li", "prompts", "cards", "docs", "notes", "source", "sources", "artifacts", "tools"]:
        if (ROOT / d).is_dir():
            wb_dirs.append(d)

    parts: list[str] = []
    parts.append("# Workbench Repo Inventory\n")
    parts.append(f"Generated: {now}\n")
    parts.append(f"Repo: {ROOT}\n")
    parts.append(f"Branch: {branch}\n")

    parts.append(section("Git Status", fence(run(["git", "status", "--short"]))))
    parts.append(section("Recent Commits", fence(run(["git", "--no-pager", "log", "--oneline", "-12"]))))

    root_inventory = run([
        "find", ".", "-maxdepth", "1", "-mindepth", "1",
        "!", "-name", ".git",
        "!", "-name", ".venv",
        "-print",
    ])
    parts.append(section("Root Inventory", fence("\n".join(sorted(root_inventory.splitlines())))))

    parts.append(section("Workbench / LI Authority Files", fence("\n".join(authority_files))))

    folder_lines: list[str] = []
    for d in wb_dirs:
        folder_lines.append("")
        folder_lines.append(f"### {d}")
        out = run([
            "find", d, "-maxdepth", "4",
            "!", "-path", "*/__pycache__/*",
            "!", "-name", "*.pyc",
            "-print",
        ])
        folder_lines.extend(sorted(out.splitlines()))
    parts.append(section("Workbench / LI Folder Structure", fence("\n".join(folder_lines))))

    make_targets = ""
    if (ROOT / "Makefile").exists():
        make_targets = run(["sh", "-c", "grep -E '^[A-Za-z0-9_.-]+:' Makefile | sed 's/:.*//' | sort -u"])
    else:
        make_targets = "(no Makefile)\n"
    parts.append(section("Makefile Targets", fence(make_targets)))

    tracked_args = [
        "git", "ls-files",
        "LLM_READ_FIRST.md", "HOW_LI_RULES.md", "SPINE.md", "MAP.md", "README.md", "Makefile",
        "LI", "li", "prompts", "cards", "docs", "notes", "source", "sources", "artifacts", "tools",
    ]
    parts.append(section("Tracked Files Under WB Folders", fence(run(tracked_args))))

    parts.append(section("Untracked Files", fence(run(["git", "ls-files", "--others", "--exclude-standard"]))))
    parts.append(section("Modified Files With Diff Stats", fence(run(["git", "diff", "--stat"]))))
    parts.append(section("Staged Files With Diff Stats", fence(run(["git", "diff", "--cached", "--stat"]))))
    parts.append(section("Ignored Files Snapshot", fence(run(["sh", "-c", "git status --ignored --short | sed -n '1,160p'"]))))

    verification = []
    verification.append("Python:")
    verification.append(run(["python3", "--version"]).strip())
    verification.append("")
    verification.append("Make verify dry-run:")
    verification.append(run(["sh", "-c", "make -n verify 2>&1 | sed -n '1,80p'"]).rstrip())
    verification.append("")
    verification.append("Make pack dry-run:")
    verification.append(run(["sh", "-c", "make -n pack 2>&1 | sed -n '1,80p'"]).rstrip())
    parts.append(section("Verification Signals", fence("\n".join(verification))))

    questions = """- Are generated inventory snapshots ignored?
- Does make verify exist and pass?
- Does make pack produce a re-entry pack?
- Is there an LI validation/governance tool?
- Are private/sensitive local artifacts ignored?
- Are authority files clear: LLM_READ_FIRST, HOW_LI_RULES, SPINE, MAP?
- Are uncommitted files intentionally separated into lanes?
"""
    parts.append(section("Known Template / Workbench Questions", questions))

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
