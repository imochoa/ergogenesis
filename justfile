set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

# Root justfile: minimal orchestration.
#   just hardware <recipe>  — ergogen + KiCad (delegates to hardware/justfile)
#   just firmware <recipe>  — ZMK firmware + keymap drawing (delegates to firmware/justfile)
#   just b                  — shortcut for `just firmware build-all`

hardware +args:
    cd hardware && just {{ args }}

firmware +args:
    cd firmware && just {{ args }}

b:
    just firmware build-all

[no-cd]
_default:
    @just --list

# [group('ci')]
fmt-just:
    @just --fmt --unstable
