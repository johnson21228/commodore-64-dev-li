#!/usr/bin/env python3
"""
Template: Capture Back apply script with review summary.

Copy this file into a generated overlay and adapt:
- OVERLAY_TITLE
- ADDED_OR_UPDATED
- REVIEW_NEXT
- OPTIONAL_REFERENCE_PATCHES

This script should apply safe repo reference updates and print a review surface.
It should not commit changes.
"""

from pathlib import Path

OVERLAY_TITLE = "Capture Back Overlay"

ADDED_OR_UPDATED = [
    ("cards/000_example_card.md", "Records the Capture Back decision."),
    ("docs/example.md", "Explains the accepted change."),
    ("li/repo/example_rule.md", "Adds the governing LI rule."),
]

REVIEW_NEXT = [
    "docs/example.md",
    "li/repo/example_rule.md",
    "CAPTURE_BACK_EXAMPLE.md",
]

SUGGESTED_VERIFY = [
    "make verify",
    "make pack",
]

SUGGESTED_COMMIT = 'git commit -m "Capture example overlay"'


def append_once(path: Path, marker: str, text: str) -> None:
    """Append text to path only if marker is not already present."""
    if not path.exists():
        return
    current = path.read_text()
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + text.strip() + "\n")


def apply_reference_patches(repo: Path) -> None:
    """Add overlay-specific MAP/README/WORKBENCH_REFERENCE patches here."""
    # Example:
    # append_once(
    #     repo / "MAP.md",
    #     "docs/example.md",
    #     "## Example\n\n- `docs/example.md`\n- `li/repo/example_rule.md`",
    # )
    pass


def print_review_summary() -> None:
    print()
    print(f"Capture Back applied: {OVERLAY_TITLE}")
    print()
    print("Added / updated:")
    for path, reason in ADDED_OR_UPDATED:
        print(f"- {path}: {reason}")
    print()
    print("Review next:")
    for path in REVIEW_NEXT:
        print(f"- {path}")
    print()
    print("Suggested verification:")
    for command in SUGGESTED_VERIFY:
        print(f"- {command}")
    print()
    print("Commit if accepted:")
    print(f"- {SUGGESTED_COMMIT}")
    print()


def main() -> None:
    repo = Path.cwd()
    apply_reference_patches(repo)
    print_review_summary()


if __name__ == "__main__":
    main()
