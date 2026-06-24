REPO_NAME := $(notdir $(CURDIR))
PACK_PATH := dist/$(REPO_NAME).pack.zip

.PHONY: verify verify-li verify-c64 verify-learning-lab history clean-li pack read-first

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


read-first:
	@cat LLM_READ_FIRST.md

.PHONY: inventory
inventory:
	python3 tools/inventory_workbench_repo.py
