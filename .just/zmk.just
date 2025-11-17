set positional-arguments := true

set shell := ["bash", "-euco", "pipefail"]

config := absolute_path('/Users/imochoa/Code/ergogenesis/config')
out := absolute_path('/Users/imochoa/Code/ergogenesis/firmware')
build := absolute_path('/Users/imochoa/Code/ergogenesis/build')
result := absolute_path('/Users/imochoa/Code/ergogenesis/result')
draw := absolute_path('/Users/imochoa/Code/ergogenesis/draw')
home_dir := env('HOME')
# user := env('USER')

# initialize west
[no-cd]
west-init:
    # git config --global --add safe.directory /workspaces/ferris-sweep-zmk-nix/zmk
    west init -l config
    west update --fetch-opt=--filter=blob:none
    west zephyr-export
    git config --global --add safe.directory ./zmk
    git config --global --add safe.directory ./zephyr

shield := "ergogenesis"

# Builds with ZMK Studio
[no-cd]
build-firmware:
    #!/usr/bin/env bash
    set -euxo pipefail

    # -p # --pristine
    #         -s "zmk/app" # the -s is not required, apparently

    build_dir="{{ build }}/left";
    mkdir -p "${build_dir}";
    west build \
        -p \
        --build-dir "${build_dir}" \
        --board "nice_nano_v2" \
        --snippet "studio-rpc-usb-uart" \
        "{{ justfile_directory() }}/zmk/app" \
        -- \
        -DZMK_CONFIG="{{ config }}" \
        -DSHIELD="{{ shield }}_left" \
        -DCONFIG_ZMK_STUDIO="y";

    if [[ -f "${build_dir}/zephyr/zmk.uf2" ]]; then
        mkdir -p "{{ out }}" && cp "${build_dir}/zephyr/zmk.uf2" "{{ out }}/zmk_left.uf2"
    fi

    build_dir="{{ build }}/right";
    mkdir -p "${build_dir}";
    west build \
        -p \
        --build-dir "${build_dir}" \
        --board "nice_nano_v2" \
        "{{ justfile_directory() }}/zmk/app" \
        -- \
        -DZMK_CONFIG="{{ config }}" \
        -DSHIELD="{{ shield }}_right";

    if [[ -f "${build_dir}/zephyr/zmk.uf2" ]]; then
        mkdir -p "{{ out }}" && cp "${build_dir}/zephyr/zmk.uf2" "{{ out }}/zmk_right.uf2"
    fi

# update west
[no-cd]
update:
    west update --fetch-opt=--filter=blob:none

# clear build cache and artifacts
[no-cd]
clean:
    rm -rf "{{ build }}" "{{ out }}"

# clear all automatically generated files
[no-cd]
clean-all: clean
    rm -rf .west zmk zephyr modules

# zmk-config := absolute_path('zmk')
#
# podman-init:
#     podman run -it --rm \
#     --security-opt label=disable \
#     --workdir /workspaces/zmk \
#     -v /path/to/zmk:/workspaces/zmk \
#     -v /path/to/zmk-config:/workspaces/zmk-config \   # Removeable
#     -v /path/to/zmk-modules:/workspaces/zmk-modules \ # Removeable
#     -p 3000:3000 \
#     <container-name> /bin/bash
