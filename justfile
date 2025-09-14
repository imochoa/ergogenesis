# Open fzf picker
[no-cd]
default:
    @just --choose

setup:
    pnpm import
    pnpm install

pnpm-build:
    pnpm run ergogen:build

pnpm-watch:
    pnpm run ergogen:watch

zmk-update:
    pnpm run zmk:update

zmk-build:
    pnpm run zmk:build

zmk-down:
    pnpm run zmk:down


visualize-dxf dxf-file="-h":
    # uv tool run 'ezdxf[draw]' view "{{dxf-file}}"
    # watchexec -e dxf -w ./ergogen/output/outlines -- uv tool run 'ezdxf[draw]' view "{{dxf-file}}"
    watchexec -r -w ./ergogen/output/outlines 'uv tool run "ezdxf[draw]" view' "{{dxf-file}}"


output-dir:="{{justfile_dir()}}/ergogen/output"
kicad-pcb:="shield-pcb"

kicad-checks:
    kicad-cli pcb drc ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # kicad-cli sch check ergogen/schematic/ergogenesis.kicad_sch
    # kicad-cli pcb check ergogen/output/pcb/ergogenesis.kicad_pc

freerouting-gui:
    # nix-shell -p freerouting --run 'freerouting'
    nix shell nixpkgs#freerouting \
        --command freerouting \
        -de "./ergogen/output/pcbs/shield-pcb.dsn" \
        -do "./ergogen/output/pcbs/shield-pcb-routed.dsn" \
        -di "./ergogen/output/pcbs/"
    # other cli args: https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md


just-check:
    just --fmt --check --unstable

just-fmt:
    just --fmt --unsafe