set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

# Root justfile: orchestration only.
#   hardware/  — ergogen + KiCad recipes (just hardware <recipe>)
#   firmware/  — ZMK firmware recipes    (just firmware <recipe>)
#   .just/draw.just — keymap layout rendering (just draw <recipe>)

mod hardware "hardware/justfile"
mod draw ".just/draw.just"

# Run a firmware recipe (delegates to firmware/justfile).
# For custom generic-build calls with empty args, use:

# cd firmware && just generic-build <board> <shield> "" "" <artifact>
firmware +args:
    cd firmware && just {{ args }}

# Shortcut for `just firmware build-all`.
b:
    just firmware build-all

# Open picker with "jj" alias
[no-cd]
_default:
    @just --list --list-submodules

# [group('ci')]
fmt-just:
    @just --fmt --unstable

# [group('ci')]
just-check:
    just --fmt --check --unstable

# [group('ci')]
just-fmt:
    just --fmt --unstable
