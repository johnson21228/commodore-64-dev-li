.PHONY: generate render polygon-proof spans span-prg verify build run run-span-prg clean moving-cube moving-byte-spans moving-byte-prg run-moving-byte-prg wasd-grid-prg run-wasd-grid-prg

generate:
	python3 tools/generate_blockout_renderer.py

render: generate
	python3 tools/render_blockout_gameboard_projection_svg.py

polygon-proof: generate
	python3 tools/render_single_cube_polygon_svg.py

spans: polygon-proof
	python3 tools/generate_single_cube_polygon_spans.py

span-prg: spans
	python3 tools/build_single_cube_span_prg.py

moving-cube: generate
	python3 tools/generate_moving_cube_same_depth_spans.py

moving-byte-spans: moving-cube
	python3 tools/generate_moving_cube_byte_spans.py

moving-byte-prg: moving-byte-spans
	python3 tools/build_moving_cube_byte_span_prg.py

build: generate
	python3 tools/build_blockout_renderer_prg.py

verify: build render polygon-proof spans span-prg moving-cube moving-byte-spans moving-byte-prg
	python3 tools/verify_blockout_projection_tables.py
	python3 tools/verify_blockout_perspective_projection.py
	python3 tools/verify_blockout_renderer_asm.py
	python3 tools/verify_blockout_gameboard_projection_svg.py
	python3 tools/verify_blockout_prg_build.py
	python3 tools/verify_blockout_single_cube_polygon.py
	python3 tools/verify_blockout_single_cube_spans.py
	python3 tools/verify_single_cube_span_prg.py
	python3 tools/verify_moving_cube_same_depth_spans.py
	python3 tools/verify_moving_cube_byte_spans.py
	python3 tools/verify_moving_cube_byte_span_prg.py

run: build
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc dist/blockout_renderer.prg; \
	elif command -v x64 >/dev/null 2>&1; then \
		x64 dist/blockout_renderer.prg; \
	else \
		echo "VICE not found. Open dist/blockout_renderer.prg with your C64 emulator."; \
	fi

clean:
	rm -rf dist/*
	rm -f src/generated_*.s

run-span-prg: span-prg
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc dist/single_cube_span_fill.prg; \
	elif command -v x64 >/dev/null 2>&1; then \
		x64 dist/single_cube_span_fill.prg; \
	else \
		echo "VICE not found. Open dist/single_cube_span_fill.prg in your C64 emulator."; \
	fi

run-moving-byte-prg: moving-byte-prg
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc dist/moving_cube_byte_span_animation.prg; \
	elif command -v x64 >/dev/null 2>&1; then \
		x64 dist/moving_cube_byte_span_animation.prg; \
	else \
		echo "VICE not found. Open dist/moving_cube_byte_span_animation.prg in your C64 emulator."; \
	fi

wasd-grid-prg: moving-byte-spans
	python3 tools/build_wasd_5x5_cube_control_prg.py

run-wasd-grid-prg: wasd-grid-prg
	@if command -v x64sc >/dev/null 2>&1; then \
		x64sc dist/wasd_5x5_cube_control.prg; \
	elif command -v x64 >/dev/null 2>&1; then \
		x64 dist/wasd_5x5_cube_control.prg; \
	else \
		echo "VICE not found. Open dist/wasd_5x5_cube_control.prg in your C64 emulator."; \
	fi

verify-piece-source:
	python3 tools/verify_blockout_piece_source.py

verify-pose-rules:
	python3 tools/verify_blockout_pose_rules.py

