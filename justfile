set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

config := absolute_path('config')
out := absolute_path('firmware')
build := absolute_path('.build')

# Firmware / ZMK recipes live here; ergogen + KiCad recipes live in the

mod in-devc ".just/in-devc.just"
mod hardware "hardware/justfile"

alias b := build-all

# Open picker with "jj" alias
[no-cd]
_default:
    @just --list --list-submodules

# [group('host')]
devc-exec +recipe:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "${container:-}" ]; then
      just devc-up
      devcontainer exec \
        --workspace-folder "{{ justfile_directory() }}" \
        --docker-path podman \
        --docker-compose-path podman-compose \
        -- bash -lc 'just "$@"' _ {{ recipe }}
    else
      bash -c 'just "$@"' _ {{ recipe }}
    fi

# [group('host')]
devc-build:
    devcontainer build \
      --workspace-folder "{{ justfile_directory() }}" \
      --docker-path podman \
      --docker-compose-path podman-compose \
      --remove-existing-container

# [group('host')]
devc-up:
    devcontainer up \
      --workspace-folder "{{ justfile_directory() }}" \
      --docker-path podman \
      --docker-compose-path podman-compose \
      --remove-existing-container
    podman ps --last 1

# [group('host')]
mkdirs:
    @just devc-exec in-devc mkdirs

# [group('host')]
hard-rmdirs:
    @just devc-exec in-devc hard-rmdirs

# initialize west

# [group('host')]
west-init:
    @just devc-exec in-devc west-init

# you might need to run this multiple times after "init"

# [group('host')]
west-update:
    @just devc-exec in-devc west-update

# update west

# [group('host')]
update:
    @just devc-exec in-devc update

# Build one firmware target (board shield snippet cmake_args artifact_name).
# snippet/cmake_args may be empty.

# [group('host')]
generic-build board shield snippet="" cmake_args="" artifact_name="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "${container:-}" ]; then
      just devc-up
      devcontainer exec \
        --workspace-folder "{{ justfile_directory() }}" \
        --docker-path podman \
        --docker-compose-path podman-compose \
        -- bash -lc 'just in-devc generic-build "$@"' _ \
        "{{ board }}" "{{ shield }}" "{{ snippet }}" "{{ cmake_args }}" "{{ artifact_name }}"
    else
      just in-devc generic-build "{{ board }}" "{{ shield }}" "{{ snippet }}" "{{ cmake_args }}" "{{ artifact_name }}"
    fi

# Builds both halves with ZMK Studio.

# [group('host')]
build-firmware: (generic-build "nice_nano_v2" "ergogenesis_left" "studio-rpc-usb-uart" "-DCONFIG_ZMK_STUDIO=y" "ergogenesis_left-nice_nano_v2-zmk") (generic-build "nice_nano_v2" "ergogenesis_right" "studio-rpc-usb-uart" "-DCONFIG_ZMK_STUDIO=y" "ergogenesis_right-nice_nano_v2-zmk")

# https://zmk.dev/docs/troubleshooting/connection-issues#reset-split-keyboard-procedure

# [group('host')]
build-settings-reset-firmware:
    just generic-build nice_nano_v2 settings_reset "" "" settings_reset-nice_nano_v2-zmk

# [group('host')]
build-all: build-firmware build-settings-reset-firmware

# [group('ci')]
fmt-just:
    @just --fmt --unstable

# [group('ci')]
just-check:
    just --fmt --check --unstable

# [group('ci')]
just-fmt:
    just --fmt --unstable
