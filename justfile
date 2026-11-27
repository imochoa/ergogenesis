set positional-arguments
set shell := ["bash", "-euco", "pipefail"]

# Root justfile: minimal orchestration.
#   just hardware <recipe>  — ergogen + KiCad (delegates to hardware/justfile)
#   just firmware <recipe>  — ZMK firmware + keymap drawing (delegates to firmware/justfile)
#   just overkeys <recipe>  — macOS on-screen keymap overlay (delegates to overkeys/justfile)
#   just b                  — shortcut for `just firmware build-all`

hardware +args:
    cd hardware && just {{ args }}

firmware +args:
    cd firmware && just {{ args }}

overkeys +args:
    cd overkeys && just {{ args }}

b:
    just firmware build-all

# [group('ci')]
renovate-logs:
    journalctl --user -u temporal-renovate-worker.service -f

renovate-logs-today:
    journalctl --user -u temporal-renovate-worker.service --since today

[no-cd]
_default:
    @just --list

# [group('ci')]
fmt-just:
    @just --fmt --unstable
