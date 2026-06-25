LAB := language_to_asm
DIST := dist
LANG := src/program.lang
INTENT := src/generated_intent.json
ASM := src/generated.s
OUT := $(DIST)/$(LAB).prg

.PHONY: build generate clean

build: $(OUT)

generate: $(ASM)

$(ASM): $(LANG) src/generate_asm.py
	python3 src/generate_asm.py $(LANG) $(INTENT) $(ASM)

$(OUT): $(ASM)
	mkdir -p $(DIST)
	cl65 -t c64 -o $(OUT) $(ASM)

clean:
	rm -rf $(DIST)
	rm -f $(INTENT) $(ASM)
