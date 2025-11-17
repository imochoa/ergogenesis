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
# mod kicad ".just/kicad.just"
# mod ergogen ".just/ergogen.just"
# mod zmk ".just/zmk.just"

# Open fzf picker
[no-cd]
_default:
    @just --choose

setup:
    pnpm import
    pnpm install

ergogen-build:
    pnpm run ergogen:build

ergogen-watch:
    pnpm run ergogen:watch

ergogen-stl-from-jscad:
    fd -ejscad . . -x npx @jscad/cli@1 "{}" -of stla -o "{.}.stl"

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
        -mt 1 \
        --router.optimizer.max_threads=0

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

# # initialize west
# west-init:
#     # git config --global --add safe.directory /workspaces/ferris-sweep-zmk-nix/zmk
#     west init -l config
#     west update --fetch-opt=--filter=blob:none
#     west zephyr-export
#     git config --global --add safe.directory ./zmk
#     git config --global --add safe.directory ./zephyr

shield := "ergogenesis"

# Builds with ZMK Studio
build-firmware-OLD:
    #!/usr/bin/env bash
    set -euxo pipefail

    # -p # --pristine
    #         -s "zmk/app" # the -s is not required, apparently
    #         CONFIG should be ABS!!

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

podman-env:
    # mkdir -p "{ mount }}/user"
    # mkdir -p "{ mount }}/zmk-config"
    # mkdir -p "{ mount }}/zmk-modules"
    # mkdir -p "{ mount }}/zmk-zephyr"
    # mkdir -p "{ mount }}/zmk-zephyr-modules"
    # mkdir -p "{ mount }}/zmk-zephyr-tools"
    mkdir -p ".build"
    mkdir -p "firmware"
    mkdir -p ".cache"
    mkdir -p ".west"
    podman run \
      --rm -it \
      --workdir /workspaces \
      -v "{{ justfile_directory() }}/config":/workspaces/config \
      -v "{{ justfile_directory() }}/zmk":/workspaces/zmk \
      -v "{{ justfile_directory() }}/zephyr":/workspaces/zephyr \
      -v "{{ justfile_directory() }}/modules":/workspaces/modules \
      -v "{{ justfile_directory() }}/tools":/workspaces/tools \
      -v "{{ justfile_directory() }}/.build":/workspaces/.build \
      -v "{{ justfile_directory() }}/.west":/workspaces/.west \
      -v "{{ justfile_directory() }}/.cache":/root/.cache \
      -v "{{ justfile_directory() }}/firmware":/workspaces/firmware \
      -v "{{ justfile_directory() }}/zmk":/workspaces/zmk \
      -v "{{ justfile_directory() }}/script.sh":/workspaces/script.sh \
      docker.io/zmkfirmware/zmk-dev-arm:3.5

devc-mkdirs:
    mkdir -p "{{ justfile_directory() }}/modules"
    mkdir -p "{{ justfile_directory() }}/zmk"
    mkdir -p "{{ justfile_directory() }}/zephyr"
    mkdir -p "{{ justfile_directory() }}/.cache"
    mkdir -p "{{ justfile_directory() }}/.build"
    mkdir -p "{{ justfile_directory() }}/.tools"
    mkdir -p "{{ justfile_directory() }}/.west"
    mkdir -p "{{ justfile_directory() }}/.home"

devc-clean-dirs: && devc-mkdirs
    rm -rf "{{ justfile_directory() }}/modules"
    rm -rf "{{ justfile_directory() }}/zmk"
    rm -rf "{{ justfile_directory() }}/zephyr"
    rm -rf "{{ justfile_directory() }}/.cache"
    rm -rf "{{ justfile_directory() }}/.build"
    rm -rf "{{ justfile_directory() }}/.tools"
    rm -rf "{{ justfile_directory() }}/.west"
    rm -rf "{{ justfile_directory() }}/.home"

# initialize west
west-init: devc-clean-dirs
    # git config --global --add safe.directory /workspaces/ferris-sweep-zmk-nix/zmk
    west init -l config
    west update --fetch-opt=--filter=blob:none
    west zephyr-export
    git config --global --add safe.directory "{{ justfile_directory() }}/zmk"
    git config --global --add safe.directory "{{ justfile_directory() }}/zephyr"

xx-west-init:
    @just devc-exec west-init

devc-full-init: devc-clean-dirs devc-build devc-up
    echo "done!"

devc-exec recipe: devc-up
    devcontainer exec \
      --workspace-folder "{{ justfile_directory() }}" \
      --docker-path podman \
      -- just {{ recipe }}

# devc-testt:
#   @just devc-exec testt
#
# testt:
#   env

devc-build:
    devcontainer build \
      --workspace-folder "{{ justfile_directory() }}" \
      --docker-path podman \
      --remove-existing-container

devc-up:
    devcontainer up \
      --workspace-folder "{{ justfile_directory() }}" \
      --docker-path podman \
      --remove-existing-container

# Builds with ZMK Studio
build-firmware:
    #!/usr/bin/env bash
    set -euxo pipefail
    # https://www.reddit.com/r/ErgoMechKeyboards/comments/1hkhyht/guide_building_zmk_firmware_locally_with_only_a/

    # that you may need to run west update a few times for everything to be fetched.
    # west init -l config && west update


    rm -rf "{{ justfile_directory() }}/firmware/*.uf2"
    # says to call it from zmk/app...
    export Zephyr_DIR="{{ justfile_directory() }}/zephyr/share/zephyr-package/cmake"

    # redo init if the paths change..., call it multiple times


    rm -rf "{{ justfile_directory() }}/.build/left"
    mkdir -p "{{ justfile_directory() }}/.build/left"
    CMAKE_PREFIX_PATH="{{ justfile_directory() }}/zephyr:\$CMAKE_PREFIX_PATH" west build \
      --pristine \
      --build-dir "{{ justfile_directory() }}/.build/left" \
      --board "nice_nano_v2" \
      --snippet "studio-rpc-usb-uart" \
      "{{ justfile_directory() }}/zmk/app" \
      -- \
      -DZMK_CONFIG="{{ justfile_directory() }}/config" \
      -DSHIELD="ergogenesis_left" \
      -DCONFIG_ZMK_STUDIO="y"

    #" west build -d /build/left -p -b "nice_nano_v2" \ -s /zmk-urchin/zmk/app \
    # -- -DSHIELD="urchin_left nice_view_adapter nice_view" \ -DZMK_CONFIG="/zmk-urchin/config" \
    # -DZMK_EXTRA_MODULES="/zmk-urchin/urchin-zmk-module"

    # -DZMK_EXTRA_MODULES="/zmk-urchin/urchin-zmk-module"

    # ZMK studio support
    # I won't go into details here. But you'd need the following extra flags in appropriate places to build a studio-compatible firmware. -S studio-rpc-usb-uart \ -DCONFIG_ZMK_STUDIO=y \

    mkdir -p "{{ justfile_directory() }}/firmware"
    if [[ -f "{{ justfile_directory() }}/.build/left/zephyr/zmk.uf2" ]]; then
      mkdir -p "{{ justfile_directory() }}/firmware" && cp "{{ justfile_directory() }}/.build/left/zephyr/zmk.uf2" "{{ justfile_directory() }}/firmware/zmk_left.uf2"
    fi

xx-build-firmware:
    @just devc-exec build-firmware

# -v "{{ mount }}/user":/root \
