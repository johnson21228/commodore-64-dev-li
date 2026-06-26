REPO_NAME := $(notdir $(CURDIR))
PACK_PATH := dist/$(REPO_NAME).pack.zip

.PHONY: verify verify-li verify-c64 verify-learning-lab verify-language-to-asm verify-pacman-bounce verify-goal-language-to-asm-net-proxy verify-net-proxy history clean-li clean-labs pack read-first inventory lab001 lab001-run lab002 lab002-run lab003 lab003-run lab004 lab004-run lab005 lab005-run lab006 lab006-run lab007 lab007-run lab008 lab008-run lab009 lab009-run lab010 lab010-run lab011 lab011-run lab011-run-net lab011-server

verify:
	python3 tools/check_template_integrity.py
	python3 tools/verify_li_governance.py
	python3 tools/verify_c64_workbench.py
	python3 tools/verify_c64_learning_lab.py
	python3 tools/verify_c64_language_to_asm.py
	python3 tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py
	python3 tools/verify_c64_goal_language_to_asm_net_proxy_lab.py

verify-li:
	python3 tools/verify_li_governance.py

verify-c64:
	python3 tools/verify_c64_workbench.py

verify-learning-lab:
	python3 tools/verify_c64_learning_lab.py

verify-language-to-asm:
	python3 tools/verify_c64_language_to_asm.py

verify-pacman-bounce:
	python3 tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py

verify-goal-language-to-asm-net-proxy:
	python3 tools/verify_c64_goal_language_to_asm_net_proxy_lab.py

verify-net-proxy:
	python3 tools/verify_c64_goal_language_to_asm_net_proxy_lab.py

history:
	python3 tools/export_repo_history_for_llm.py

clean-li:
	python3 tools/clean_li_repo_artifacts.py

clean-labs:
	find labs -path "*/dist" -type d -prune -exec rm -rf {} +
	find labs -name "*.o" -type f -delete

pack: history clean-li
	mkdir -p dist
	rm -f "$(PACK_PATH)"
	zip -r "$(PACK_PATH)" . 		-x ".git/*" 		-x ".git/**" 		-x "dist/*.zip" 		-x "artifacts/workbench_repo_inventory_*.md" 		-x "labs/*/dist/*" 		-x "labs/*/src/*.o" 		-x "__pycache__/*" 		-x "*/__pycache__/*" 		-x ".DS_Store" 		-x "__MACOSX/*"
	@echo "Wrote $(PACK_PATH)"

lab001:
	$(MAKE) -C labs/001_hello_screen build

lab001-run: lab001
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/001_hello_screen/dist/hello_screen.prg; else echo "x64sc not found. Install VICE or open labs/001_hello_screen/dist/hello_screen.prg manually."; exit 1; fi

lab002:
	$(MAKE) -C labs/002_screen_memory build

lab002-run: lab002
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/002_screen_memory/dist/screen_memory.prg; else echo "x64sc not found. Install VICE or open labs/002_screen_memory/dist/screen_memory.prg manually."; exit 1; fi

lab003:
	$(MAKE) -C labs/003_color_memory build

lab003-run: lab003
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/003_color_memory/dist/color_memory.prg; else echo "x64sc not found. Install VICE or open labs/003_color_memory/dist/color_memory.prg manually."; exit 1; fi

lab004:
	$(MAKE) -C labs/004_petscii_ui build

lab004-run: lab004
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/004_petscii_ui/dist/petscii_ui.prg; else echo "x64sc not found. Install VICE or open labs/004_petscii_ui/dist/petscii_ui.prg manually."; exit 1; fi

lab005:
	$(MAKE) -C labs/005_keyboard_input build

lab005-run: lab005
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/005_keyboard_input/dist/keyboard_input.prg; else echo "x64sc not found. Install VICE or open labs/005_keyboard_input/dist/keyboard_input.prg manually."; exit 1; fi

lab006:
	$(MAKE) -C labs/006_sprite_basics build

lab006-run: lab006
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/006_sprite_basics/dist/sprite_basics.prg; else echo "x64sc not found. Install VICE or open labs/006_sprite_basics/dist/sprite_basics.prg manually."; exit 1; fi

lab007:
	$(MAKE) -C labs/007_sid_tone build

lab007-run: lab007
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/007_sid_tone/dist/sid_tone.prg; else echo "x64sc not found. Install VICE or open labs/007_sid_tone/dist/sid_tone.prg manually."; exit 1; fi

lab008:
	$(MAKE) -C labs/008_memory_pal build

lab008-run: lab008
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/008_memory_pal/dist/memory_pal.prg; else echo "x64sc not found. Install VICE or open labs/008_memory_pal/dist/memory_pal.prg manually."; exit 1; fi

lab009:
	$(MAKE) -C labs/009_language_to_asm build

lab009-run: lab009
	@if command -v x64sc >/dev/null 2>&1; then x64sc labs/009_language_to_asm/dist/language_to_asm.prg; else echo "x64sc not found. Install VICE or open labs/009_language_to_asm/dist/language_to_asm.prg manually."; exit 1; fi

lab010:
	$(MAKE) -C labs/010_goal_language_to_asm_pacman_bounce build

lab010-run: lab010
	@if command -v x64sc >/dev/null 2>&1; then PRG=$$(find labs/010_goal_language_to_asm_pacman_bounce/dist -name "*.prg" | head -1); if [ -n "$$PRG" ]; then x64sc "$$PRG"; else echo "No Lab 010 PRG found under labs/010_goal_language_to_asm_pacman_bounce/dist"; exit 1; fi; else echo "x64sc not found. Install VICE or open the Lab 010 PRG manually."; exit 1; fi

lab011:
	$(MAKE) -C labs/011_goal_language_to_asm_net_proxy build

lab011-run: lab011
	@if command -v x64sc >/dev/null 2>&1; then PRG=$$(find labs/011_goal_language_to_asm_net_proxy/dist -name "*.prg" | head -1); if [ -n "$$PRG" ]; then x64sc "$$PRG"; else echo "No Lab 011 PRG found under labs/011_goal_language_to_asm_net_proxy/dist"; exit 1; fi; else echo "x64sc not found. Install VICE or open the Lab 011 PRG manually."; exit 1; fi

lab011-run-net: lab011
	$(MAKE) -C labs/011_goal_language_to_asm_net_proxy run-net

lab011-server:
	python3 labs/011_goal_language_to_asm_net_proxy/host/proxy_server.py

read-first:
	@cat LLM_READ_FIRST.md

inventory:
	python3 tools/inventory_workbench_repo.py
