REPO_NAME := $(notdir $(CURDIR))
PACK_PATH := dist/$(REPO_NAME).pack.zip

.PHONY: verify verify-li verify-c64 verify-learning-lab lab001 lab001-run lab002 lab002-run lab003 lab003-run history clean-li pack read-first

verify:
	python3 tools/check_template_integrity.py
	python3 tools/verify_li_governance.py
	python3 tools/verify_c64_workbench.py
	python3 tools/verify_c64_learning_lab.py

verify-li:
	python3 tools/verify_li_governance.py

verify-c64:
	python3 tools/verify_c64_workbench.py

verify-learning-lab:
	python3 tools/verify_c64_learning_lab.py

history:
	python3 tools/export_repo_history_for_llm.py

clean-li:
	python3 tools/clean_li_repo_artifacts.py

pack: history clean-li
	mkdir -p dist
	rm -f "$(PACK_PATH)"
	zip -r "$(PACK_PATH)" . \
		-x ".git/*" \
		-x ".git/**" \
		-x "dist/*.zip" \
		-x "artifacts/workbench_repo_inventory_*.md" \
		-x "__pycache__/*" \
		-x "*/__pycache__/*" \
		-x ".DS_Store" \
		-x "__MACOSX/*"
	@echo "Wrote $(PACK_PATH)"



lab001:
	$(MAKE) -C labs/001_hello_screen build

lab001-run: lab001
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc labs/001_hello_screen/dist/hello_screen.prg; \
	else \
		echo "x64sc not found. Install VICE or open labs/001_hello_screen/dist/hello_screen.prg manually in your C64 emulator."; \
		exit 1; \
	fi

lab002:
	$(MAKE) -C labs/002_screen_memory build

lab002-run: lab002
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc labs/002_screen_memory/dist/screen_memory.prg; \
	else \
		echo "x64sc not found. Install VICE or open labs/002_screen_memory/dist/screen_memory.prg manually in your C64 emulator."; \
		exit 1; \
	fi

lab003:
	$(MAKE) -C labs/003_color_memory build

lab003-run: lab003
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc labs/003_color_memory/dist/color_memory.prg; \
	else \
		echo "x64sc not found. Install VICE or open labs/003_color_memory/dist/color_memory.prg manually in your C64 emulator."; \
		exit 1; \
	fi

read-first:
	@cat LLM_READ_FIRST.md

.PHONY: inventory
inventory:
	python3 tools/inventory_workbench_repo.py
