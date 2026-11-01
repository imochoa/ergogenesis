set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

# This module renders the ZMK keymap as an SVG and converts it to PDF.
# Run from the repo root via `just firmware draw <recipe>`.

draw := justfile_dir() / "draw"
outputs := justfile_dir() / "outputs"
config := justfile_dir() / "config"
# keymap_file := config / "boards/shields/ergogenesis/ergogenesis.keymap"
keymap_file := config / "ergogenesis.keymap"

# keymap-drawer ships a `keymap` CLI (PyPI package `keymap-drawer`, so `--from`).
# Run it via uvx with a clean env so the host's PYTHONPATH (from the nix dev
# shell) doesn't leak into uvx's interpreter and break pydantic imports.

keymap := "env -u PYTHONPATH -u PYTHONHOME uvx --from keymap-drawer keymap"

# Parse the ZMK keymap into YAML (intermediate step; writes draw/base.yaml).
[no-cd]
parse:
    #!/usr/bin/env bash
    set -euo pipefail
    {{ keymap }} -c "{{ draw }}/config.yaml" parse -z "{{ keymap_file }}" >"{{ draw }}/base.yaml"

# Draw the keymap SVG from the parsed YAML (writes outputs/base.svg).

# Uses a parametrized ortho layout: 5 cols × 3 rows + 3 thumbs per side (36 keys).
[no-cd]
draw-svg: parse
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p "{{ outputs }}"
    {{ keymap }} -c "{{ draw }}/config.yaml" draw -n "33333+3 3+33333" "{{ draw }}/base.yaml" >"{{ outputs }}/base.svg"

# Convert the keymap SVG to a PDF (writes outputs/base.pdf).
[no-cd]
svg-to-pdf: draw-svg
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p "{{ outputs }}"
    nix shell nixpkgs#librsvg --command rsvg-convert -f pdf -o "{{ outputs }}/base.pdf" "{{ outputs }}/base.svg"

# Render the keymap to SVG and convert to PDF (writes outputs/base.svg + base.pdf).
[no-cd]
draw-pdf: svg-to-pdf
    @echo "wrote {{ outputs }}/base.svg and {{ outputs }}/base.pdf"

# Parse & plot keymap (alias of draw-svg).
[no-cd]
draw: draw-svg

# Watch the keymap + config and re-render the SVG on changes.
[no-cd]
watch:
    #!/usr/bin/env bash
    set -euo pipefail
    find "{{ config }}/" -name '.*' -prune -o -print | entr -cd just --justfile "{{ justfile_dir() }}/justfile" draw draw-svg
