APP := pacman_bounce
SRC_DIR := src
DIST_DIR := dist
ASM := $(SRC_DIR)/generated.s
INTENT := $(SRC_DIR)/generated_intent.json
GOAL := $(SRC_DIR)/goal.lang
PROGRAM := $(SRC_DIR)/program.lang
BOARD := $(SRC_DIR)/board.txt
PROJECTED_BOARD := $(SRC_DIR)/projected_board.json
PRG := $(DIST_DIR)/$(APP).prg

.PHONY: build run clean regenerate verify-board

build: $(PRG)

$(ASM) $(INTENT): $(GOAL) $(PROGRAM) $(BOARD) $(PROJECTED_BOARD) $(SRC_DIR)/generate_asm.py
	python3 $(SRC_DIR)/generate_asm.py $(GOAL) $(PROGRAM) $(INTENT) $(ASM)

$(PRG): $(ASM) c64_asm.cfg
	mkdir -p $(DIST_DIR)
	cl65 -C c64_asm.cfg -o $(PRG) $(ASM)

verify-board:
	python3 $(SRC_DIR)/verify_projected_board.py

run: build
	@if command -v x64sc >/dev/null 2>&1; then x64sc $(PRG); else echo "x64sc not found. Install VICE or open $(PRG) manually."; fi

regenerate:
	python3 $(SRC_DIR)/generate_asm.py $(GOAL) $(PROGRAM) $(INTENT) $(ASM)

clean:
	rm -rf $(DIST_DIR)
	rm -f $(SRC_DIR)/*.o
