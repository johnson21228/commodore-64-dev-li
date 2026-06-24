#!/usr/bin/env python3
from pathlib import Path

required = [
    "LLM_READ_FIRST.md",
    "MAP.md",
    "HOW_LI_RULES.md",
    "li/workflow/workbench_build_loop.md",
    "li/continuity_notes.md",
    "li/source/source_truth.md",
    "tools/verify_li_governance.py",
    "README.md",
    "SPINE.md",
    "Makefile",
    "prompts/00_create_a_workbench_li_repo.md",
    "prompts/07_interpret_repo_history_briefly.md",
    "tools/export_repo_history_for_llm.py",
    "tools/clean_li_repo_artifacts.py",
    "prompts/generate_newcomer_workbench_loop_infographic.md",
    "docs/newcomer_workbench_loop_infographic.md",
    "li/workflow/newcomer_infographic_contract.md",
]
missing = [p for p in required if not Path(p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f"- {p}")
    raise SystemExit(1)

readme = Path("README.md").read_text(encoding="utf-8")
for forbidden in [
    "# Workbench Completion Modes Overlay",
    "Adds LI and prompt guidance for three completion modes",
    "# Capture Back Nomenclature Overlay",
    "Updates the Workbench Loop language so the conceptual step is **Capture Back**",
]:
    if forbidden in readme:
        print("README.md still contains overlay-starter residue:")
        print(f"- {forbidden}")
        raise SystemExit(1)

makefile = Path("Makefile").read_text(encoding="utf-8")
if '-x "*.git*"' in makefile:
    print('Makefile pack rule uses broad "*.git*" exclusion; this can drop .gitignore from starter packs.')
    raise SystemExit(1)
if '-x ".git/*"' not in makefile:
    print('Makefile pack rule should exclude the .git directory without excluding .gitignore.')
    raise SystemExit(1)

loop_files = [
    "README.md",
    "docs/workbench_build_loop_infographic.md",
    "docs/workbench_loop_simple_infographic.md",
    "prompts/generate_simple_workbench_loop_infographic.md",
    "prompts/generate_workbench_build_loop_infographic.md",
    "li/workflow/high_level_workbench_loop.md",
    "li/workflow/workbench_build_loop.md",
    "li/workflow/visible_workflow_outcome_contract.md",
]
for path_text in loop_files:
    path = Path(path_text)
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    for forbidden in [
        "Pack → Reason → Overlay",
        "Generate Overlay",
        "Generate an Overlay",
        "Ask for overlay",
        "Ask for an overlay",
        "overlay → terminal",
        "reasoning → overlay",
    ]:
        if forbidden in text:
            print(f"{path_text} still uses overlay as the Workbench Loop concept:")
            print(f"- {forbidden}")
            raise SystemExit(1)

print("Workbench LI template integrity check passed.")


# Workbench Loop infographic quality guard
from pathlib import Path as _Path
for _asset in [
]:
    if not _asset.exists():
        raise SystemExit(f"Missing required JPEG infographic asset: {_asset}")
    if _asset.stat().st_size < 50_000:
        raise SystemExit(f"Infographic asset looks too small / placeholder-like: {_asset}")

for _old in [
]:
    if _old.exists():
        raise SystemExit(f"SVG-only Workbench Loop asset should not be the consumer-facing default: {_old}")

for _file in [
]:
    if _file.exists():
        _text = _file.read_text()
        if "Capture Back" not in _text:
            raise SystemExit(f"Missing Capture Back language in {_file}")

# Prompt-only infographic Capture Back guard.
for rel in [
    "prompts/generate_newcomer_workbench_loop_infographic.md",
    "prompts/generate_newcomer_multi_pack_workbench_loop_infographic.md",
    "li/workflow/infographic_prompt_only_capture_back.md",
]:
    if not Path(rel).exists():
        fail(f"missing prompt-only infographic guidance: {rel}")

for rel in [
    "docs/assets/workbench_loop_newcomer.jpg",
    "docs/assets/workbench_loop_multi_pack.jpg",
    "docs/assets/workbench_loop_newcomer.svg",
    "docs/assets/workbench_loop_multi_pack.svg",
]:
    if Path(rel).exists():
        fail(f"generated/fixed infographic asset should not be captured by default: {rel}")

# Capture Back apply command hardening checks
for rel in [
    "li/repo/capture_back_apply_command_hardening.md",
    "prompts/generate_capture_back_overlay_apply_command.md",
    "notes/capture_back_apply_command_failure_lesson.md",
]:
    if not Path(rel).exists():
        raise SystemExit(f"Missing Capture Back apply command hardening file: {rel}")



# Workbench Loop re-entry protocol must remain available.
for required_path in [
    "li/workflow/workbench_loop_reentry_protocol.md",
    "prompts/rejoin_unfinished_workbench_loop.md",
    "notes/workbench_loop_reentry_lesson.md",
]:
    if not Path(required_path).exists():
        raise SystemExit(f"Missing Workbench Loop re-entry file: {required_path}")


# Capture Back apply commands must include root-detection guidance.
for required_path in [
    "li/repo/capture_back_root_detection_rule.md",
    "prompts/generate_hardened_capture_back_apply_command.md",
    "notes/capture_back_root_detection_lesson.md",
]:
    if not Path(required_path).exists():
        raise SystemExit(f"Missing Capture Back root-detection file: {required_path}")


# Team member onboarding protocol must remain available.
for required_path in [
    "li/workflow/team_member_onboarding_protocol.md",
    "docs/onboarding_a_new_team_member.md",
    "prompts/simulate_new_team_member_onboarding.md",
    "prompts/write_first_read_reaction_note.md",
    "notes/team_member_onboarding_capture_back_lesson.md",
]:
    if not Path(required_path).exists():
        raise SystemExit(f"Missing team member onboarding file: {required_path}")
