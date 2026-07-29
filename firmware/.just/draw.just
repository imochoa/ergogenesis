set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

# This module renders the ZMK keymap as an SVG and converts it to PDF.
# Run from the repo root via `just firmware draw <recipe>`.

draw := justfile_dir() / "draw"
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

# Draw the keymap SVG from the parsed YAML (writes draw/base.svg).

# Uses a parametrized ortho layout: 5 cols × 3 rows + 3 thumbs per side (36 keys).
[no-cd]
draw-svg: parse
    #!/usr/bin/env bash
    set -euo pipefail
    {{ keymap }} -c "{{ draw }}/config.yaml" draw -n "33333+3 3+33333" "{{ draw }}/base.yaml" >"{{ draw }}/base.svg"

# Convert the keymap SVG to a PDF (writes draw/base.pdf).
[no-cd]
svg-to-pdf:
    #!/usr/bin/env bash
    set -euo pipefail
    nix shell nixpkgs#librsvg --command rsvg-convert -f pdf -o "{{ draw }}/base.pdf" "{{ draw }}/base.svg"

# Render the keymap to SVG and convert to PDF (writes draw/base.svg + base.pdf).
[no-cd]
draw-pdf: draw-svg svg-to-pdf
    @echo "wrote {{ draw }}/base.svg and {{ draw }}/base.pdf"

# Parse & plot keymap (alias of draw-svg).
[no-cd]
draw: draw-svg

# Watch the keymap + config and re-render the SVG on changes.
[no-cd]
watch:
    #!/usr/bin/env bash
    set -euo pipefail
    find "{{ config }}/" -name '.*' -prune -o -print | entr -cd just firmware draw draw-svg
