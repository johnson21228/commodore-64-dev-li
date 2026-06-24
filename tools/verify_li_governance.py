#!/usr/bin/env python3
from pathlib import Path
import sys

REQUIRED = [
    "LLM_READ_FIRST.md",
    "MAP.md",
    "HOW_LI_RULES.md",
    "SPINE.md",
    "li/core/workbench_principles.md",
    "li/core/human_custody.md",
    "li/core/llm_role.md",
    "li/core/generated_artifacts_are_evidence.md",
    "li/continuity_notes.md",
    "li/workflow/workbench_build_loop.md",
    "li/workflow/high_level_workbench_loop.md",
    "li/workflow/visible_workflow_outcome_contract.md",
    "li/source/source_truth.md",
    "li/source/source_context_map.md",
    "li/source/authority_levels.md",
    "li/repo/history_pattern.md",
    "li/repo/overlay_workflow.md",
    "li/repo/fresh_terminal_apply_command.md",
    "li/repo/fail_closed_apply_command.md",
    "li/repo/generated_artifact_commit_order.md",
    "li/repo/completion_modes.md",
    "li/repo/token_discipline.md",
    "li/repo/github_workflow.md",
    "li/repo/packaging_contract.md",
    "li/repo/clean_pack_rebuild_contract.md",
    "li/repo/cleanup_contract.md",
    "li/repo/verification_contract.md",
    "docs/workbench_build_loop_infographic.md",
    "docs/workbench_loop_simple_infographic.md",
    "prompts/llm_read_first_repo_governance.md",
    "prompts/apply_overlay_terminal_workflow.md",
    "prompts/apply_command_fresh_terminal.md",
    "prompts/apply_command_fail_closed.md",
    "prompts/apply_command_generated_artifact_order.md",
    "prompts/choose_workbench_completion_mode.md",
    "prompts/generate_simple_workbench_loop_infographic.md",
    "prompts/convert_existing_repo_to_workbench_li.md",
    "prompts/evaluate_workbench_against_existing_tools.md",
    "tools/export_repo_history_for_llm.py",
    "tools/clean_li_repo_artifacts.py",
]

def main() -> int:
    missing = [p for p in REQUIRED if not Path(p).exists()]
    if missing:
        print("Missing Workbench LI governance files:")
        for p in missing:
            print(f"- {p}")
        return 1

    generated_contract = Path("li/core/generated_artifacts_are_evidence.md").read_text(encoding="utf-8")
    if "evidence only" not in generated_contract.lower():
        print("Generated-artifact contract does not clearly say evidence only.")
        return 1

    map_text = Path("MAP.md").read_text(encoding="utf-8")
    for token in ["LLM_READ_FIRST.md", "li/workflow/workbench_build_loop.md", "tools/verify_li_governance.py"]:
        if token not in map_text:
            print(f"MAP.md does not reference {token}")
            return 1

    print("Workbench LI governance verification passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
