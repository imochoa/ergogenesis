set positional-arguments := true

# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unbound variables as an error when substituting.
# -c If set, commands are read from string. This option is used to provide commands that don't come from a file.
# -o pipefail If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline.

set shell := ["bash", "-euco", "pipefail"]


config := absolute_path('config')
out := absolute_path('firmware')
build := absolute_path('.build')
result := absolute_path('result')
draw := absolute_path('draw')
home_dir := env('HOME')
# user := env('USER')


# Open fzf picker
[no-cd]
default:
    @just --choose

setup:
    pnpm import
    pnpm install

ergogen-build:
    pnpm run ergogen:build

ergogen-watch:
    pnpm run ergogen:watch

ergogen-zmk-update:
    pnpm run zmk:update

ergogen-zmk-build:
    pnpm run zmk:build

ergogen-zmk-down:
    pnpm run zmk:down

# Case!
# npx @jscad/cli@1 output/cases/bottom.jscad -of stla -o bottom.stl
# 4mm M2 screws

visualize-dxf dxf-file="-h":
    # uv tool run 'ezdxf[draw]' view "{{ dxf-file }}"
    # watchexec -e dxf -w ./ergogen/output/outlines -- uv tool run 'ezdxf[draw]' view "{{ dxf-file }}"
    watchexec -r -w ./ergogen/output/outlines 'uv tool run "ezdxf[draw]" view' "{{ dxf-file }}"

output-dir := "{{justfile_dir()}}/ergogen/output"
kicad-pcb := "shield-pcb"

kicad-checks:
    kicad-cli pcb drc ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # kicad-cli sch check ergogen/schematic/ergogenesis.kicad_sch
    # kicad-cli pcb check ergogen/output/pcb/ergogenesis.kicad_pc

kicad-freerouting-gui:
    # nix-shell -p freerouting --run 'freerouting'
    nix shell nixpkgs#freerouting \
        --command freerouting \
        -da \
        -de "./ergogen/output/manual/shield-pcb.dsn" \
        -do "./ergogen/output/manual/shield-pcb-routed.ses" \
        -di "./ergogen/output/manual/" \
        -inc GND \
        -mt 1
    # other cli args: https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md
    #  --gui.enabled=false
    # other settings: https://github.com/freerouting/freerouting/blob/master/docs/settings.md

    # has api server! use from Kicad?

kicad-export-pdf:
    # front
    kicad-cli pcb export pdf \
        -l F.Cu,F.Adhesive,F.Paste,F.Silkscreen,F.Mask,F.Courtyard,F.Fab,Edge.Cuts \
        --output pcb-FRONT.pdf \
        --black-and-white \
        --include-border-title \
        ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # back
    kicad-cli pcb export pdf \
        -l B.Cu,B.Adhesive,B.Paste,B.Silkscreen,B.Mask,B.Courtyard,B.Fab,Edge.Cuts \
        --output pcb-BACK.pdf \
        --black-and-white \
        --include-border-title \
        ./ergogen/output/pcbs/shield-pcb.kicad_pcb

just-check:
    just --fmt --check --unstable

just-fmt:
    just --fmt --unstable



# initialize west
west-init:
    # git config --global --add safe.directory /workspaces/ferris-sweep-zmk-nix/zmk
    west init -l config
    west update --fetch-opt=--filter=blob:none
    west zephyr-export
    git config --global --add safe.directory ./zmk
    git config --global --add safe.directory ./zephyr

shield := "ergogenesis"

# Builds with ZMK Studio
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
update:
    west update --fetch-opt=--filter=blob:none

# clear build cache and artifacts
clean:
    rm -rf {{ build }} {{ out }}

# clear all automatically generated files
clean-all: clean
    rm -rf .west zmk zephyr modules

