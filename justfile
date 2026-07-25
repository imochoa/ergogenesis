set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

config := absolute_path('config')
out := absolute_path('firmware')
build := absolute_path('.build')
result := absolute_path('result')
draw := absolute_path('draw')
home_dir := env('HOME')

# mod draw ".just/draw.just"

mod in-devc ".just/in-devc.just"

alias b := build-all

# Open picker with "jj" alias
[no-cd]
_default:
    @just --list --list-submodules

[group('ergogen')]
setup:
    pnpm import
    pnpm install

[group('ergogen')]
ergogen-build:
    pnpm run ergogen:build

[group('ergogen')]
ergogen-watch:
    pnpm run ergogen:watch

# [group('ergogen')]
ergogen-stl-from-jscad:
    fd -ejscad . . -x npx @jscad/cli@1 "{}" -of stla -o "{.}.stl"

# [group('ergogen')]

# visualize-dxf dxf-file="./ergogen/output/outlines/combo_ol.dxf":
visualize-dxf dxf-file="./ergogen/output/outlines/stack_ol.dxf":
    # uv tool run 'ezdxf[draw]' view "{{ dxf-file }}"
    # uv tool run "ezdxf[draw]" view  ./ergogen/output/outlines/combo_ol.dxf
    # watchexec -e dxf -w ./ergogen/output/outlines -- uv tool run 'ezdxf[draw]' view "{{ dxf-file }}"
    watchexec -r -w ./ergogen/output/outlines 'uv tool run "ezdxf[draw]" view "{{ dxf-file }}"'

output-dir := "{{justfile_dir()}}/ergogen/output"
kicad-pcb := "shield-pcb"

[group('kicad')]
kicad-checks:
    kicad-cli pcb drc ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # kicad-cli sch check ergogen/schematic/ergogenesis.kicad_sch
    # kicad-cli pcb check ergogen/output/pcb/ergogenesis.kicad_pc

# Run DRC with AISLER manufacturer rules.
# Profiles: aisler-2L-simple, aisler-2L-hd (default), aisler-4L-hd

# Rules from ergogen/drc/*.kicad_dru (downloaded from AislerHQ/aisler-support).
[group('kicad')]
kicad-drc-aisler profile="aisler-2L-hd" pcb="./ergogen/manual/shield-pcb.kicad_pcb":
    #!/usr/bin/env python3
    import json, shutil, os, subprocess, sys

    pcb      = "{{ pcb }}"
    profile  = "{{ profile }}"
    base     = os.path.splitext(pcb)[0]
    pro_path = base + ".kicad_pro"
    dru_dst  = base + ".kicad_dru"
    dru_src  = "./ergogen/drc/" + profile + ".kicad_dru"

    rules_map = {
        "aisler-2L-simple": {"min_clearance": 0.15,  "min_track_width": 0.2,   "min_via_diameter": 0.7,  "min_via_annular_width": 0.2,  "min_through_hole_diameter": 0.3},
        "aisler-2L-hd":     {"min_clearance": 0.125, "min_track_width": 0.125, "min_via_diameter": 0.45, "min_via_annular_width": 0.1,  "min_through_hole_diameter": 0.25},
        "aisler-4L-hd":     {"min_clearance": 0.125, "min_track_width": 0.125, "min_via_diameter": 0.45, "min_via_annular_width": 0.1,  "min_through_hole_diameter": 0.25},
    }
    if profile not in rules_map:
        print(f"Unknown profile '{profile}'. Choose from: {', '.join(rules_map)}")
        sys.exit(1)

    # Back up existing .kicad_pro, patch with AISLER rules
    backed_up = os.path.exists(pro_path)
    if backed_up:
        shutil.copy2(pro_path, pro_path + ".bak")
        d = json.load(open(pro_path))
    else:
        d = {"board": {"design_settings": {"rules": {}}}}
    d["board"]["design_settings"]["rules"].update(rules_map[profile])
    json.dump(d, open(pro_path, "w"), indent=2)

    # Copy custom DRC rules (.kicad_dru)
    shutil.copy2(dru_src, dru_dst)

    # Run DRC
    print(f"=== DRC with {profile} rules on {pcb} ===")
    result = subprocess.run(["kicad-cli", "pcb", "drc", "--exit-code-violations", "--severity-error", pcb],
                            capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Restore originals
    if backed_up:
        shutil.move(pro_path + ".bak", pro_path)
    else:
        os.remove(pro_path)
    os.remove(dru_dst)

    sys.exit(result.returncode)

# [group('kicad')]
kicad-freerouting-gui:
    # nix-shell -p freerouting --run 'freerouting'
    #
    # NOTE: multi-threaded route optimization is currently broken upstream —
    # Freerouting logs "Multi-threaded route optimization is broken and it is
    # known to generate clearance violations" and explicitly recommends `-mt 1`.
    # So leave threads at 1 regardless of core count (the M4 has plenty of headroom;
    # this keyboard PCB routes in well under a minute).
    #
    # `-mt 0` / `router.max_threads=0` would DISABLE optimization entirely — do not use.
    # `router.optimizer.max_threads` is not a real key (no `optimizer.` subgroup under `router`).
    #
    # `-inc GND`: let the B.Cu ground pour handle GND, not the autorouter.
    #   KiCad exports the zone outline as a Specctra `plane` regardless of fill
    #   state, so leave the zone unfilled, route, import the .ses, then fill in KiCad
    #   and run DRC (`just kicad-checks`).
    nix shell nixpkgs#freerouting \
        --command freerouting \
        -da \
        -de "./ergogen/manual/shield-pcb.dsn" \
        -do "./ergogen/manual/shield-pcb-routed.ses" \
        -di "./ergogen/manual/" \
        -inc GND \
        -mt 1 \
        --router.optimizer.max_threads=0 \
        -us global \
        -oit 0

# other cli args: https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md
#  --gui.enabled=false
# other settings: https://github.com/freerouting/freerouting/blob/master/docs/settings.md
# has api server! use from Kicad?

# [group('kicad')]
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

# [group('ci')]
just-check:
    just --fmt --check --unstable

# [group('ci')]
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

# [group('zmk')]
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

# # update west
# [group('zmk')]
# update:
#     west update --fetch-opt=--filter=blob:none
# # clear build cache and artifacts
# [group('zmk')]
# clean:
#     rm -rf {{ build }} {{ out }}
# # clear all automatically generated files
# [group('zmk')]
# clean-all: clean
#     rm -rf .west zmk zephyr modules

# [group('zmk')]
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

# [group('zmk')]
# devc-mkdirs:
#     mkdir -p "{{ justfile_directory() }}/modules"
#     mkdir -p "{{ justfile_directory() }}/zmk"
#     mkdir -p "{{ justfile_directory() }}/zephyr"
#     mkdir -p "{{ justfile_directory() }}/.cache"
#     mkdir -p "{{ justfile_directory() }}/.build"
#     mkdir -p "{{ justfile_directory() }}/.tools"
#     mkdir -p "{{ justfile_directory() }}/.home"
#     # should be made via the init recipe: .west
#     # mkdir -p "{{ justfile_directory() }}/.west"
# [group('zmk')]
# devc-clean-dirs: && devc-mkdirs
#     rm -rf "{{ justfile_directory() }}/modules"
#     rm -rf "{{ justfile_directory() }}/zmk"
#     rm -rf "{{ justfile_directory() }}/zephyr"
#     rm -rf "{{ justfile_directory() }}/.cache"
#     rm -rf "{{ justfile_directory() }}/.build"
#     rm -rf "{{ justfile_directory() }}/.tools"
#     rm -rf "{{ justfile_directory() }}/.west"
#     rm -rf "{{ justfile_directory() }}/.home"
# # initialize west
# [group('zmk')]
# west-init: devc-clean-dirs
#     # git config --global --add safe.directory /workspaces/ferris-sweep-zmk-nix/zmk
#     west init -l config
#     west update --fetch-opt=--filter=blob:none
#     west zephyr-export
#     git config --global --add safe.directory "{{ justfile_directory() }}/zmk"
#     git config --global --add safe.directory "{{ justfile_directory() }}/zephyr"
# [group('zmk')]
# xx-west-init:
#     @just devc-exec west-init
# [group('zmk')]
# devc-full-init: devc-clean-dirs devc-build devc-up
#     echo "done!"
# [group('zmk')]
# devc-exec recipe: devc-up
#     devcontainer exec \
#       --workspace-folder "{{ justfile_directory() }}" \
#       --docker-path podman \
#       -- just {{ recipe }}
# devc-testt:
#   @just devc-exec testt
#
# testt:
#   env
# [group('zmk')]
# devc-build:
#     devcontainer build \
#       --workspace-folder "{{ justfile_directory() }}" \
#       --docker-path podman \
#       --remove-existing-container
# [group('zmk')]
# devc-up:
#     devcontainer up \
#       --workspace-folder "{{ justfile_directory() }}" \
#       --docker-path podman \
#       --remove-existing-container
# # Builds with ZMK Studio
# [group('zmk')]
# build-firmware:
#     #!/usr/bin/env bash
#     set -euxo pipefail
#     # https://www.reddit.com/r/ErgoMechKeyboards/comments/1hkhyht/guide_building_zmk_firmware_locally_with_only_a/
#     # that you may need to run west update a few times for everything to be fetched.
#     # west init -l config && west update
#     out="{{ justfile_directory() }}/firmware"
#     mkdir -p "${out}"
#     rm -rf "${out}/*.uf2"
#     # says to call it from zmk/app...
#     export Zephyr_DIR="{{ justfile_directory() }}/zephyr/share/zephyr-package/cmake"
#     for side in "left" "right"; do
#       build="{{ justfile_directory() }}/.build/${side}"
#       echo "${side}"
#       echo "${build}"
#       rm -rf "${build}"
#       mkdir -p "${build}"
#       CMAKE_PREFIX_PATH="{{ justfile_directory() }}/zephyr:\$CMAKE_PREFIX_PATH" west build \
#         --pristine \
#         --build-dir "${build}" \
#         --board "nice_nano_v2" \
#         --snippet "studio-rpc-usb-uart" \
#         "{{ justfile_directory() }}/zmk/app" \
#         -- \
#         -DZMK_CONFIG="{{ justfile_directory() }}/config" \
#         -DSHIELD="ergogenesis_${side}" \
#         -DCONFIG_ZMK_STUDIO="y"
#       if [[ -f "${build}/zephyr/zmk.uf2" ]]; then
#         cp "${build}/zephyr/zmk.uf2" "${out}/zmk_${side}.uf2"
#       fi
#     done
#     # redo init if the paths change..., call it multiple times
# [group('zmk')]
# xx-build-firmware:
#     @just devc-exec build-firmware

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
    # cd .just/ && just --fmt --unstable
