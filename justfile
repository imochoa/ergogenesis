set positional-arguments := true

# -e Exit immediately if a command exits with a non-zero status.
# -u Treat unbound variables as an error when substituting.
# -c If set, commands are read from string. This option is used to provide commands that don't come from a file.
# -o pipefail If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline.

set shell := ["bash", "-euco", "pipefail"]


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
    # uv tool run 'ezdxf[draw]' view "{{ dxf-file }}"
    # watchexec -e dxf -w ./ergogen/output/outlines -- uv tool run 'ezdxf[draw]' view "{{ dxf-file }}"
    watchexec -r -w ./ergogen/output/outlines 'uv tool run "ezdxf[draw]" view' "{{ dxf-file }}"

output-dir := "{{justfile_dir()}}/ergogen/output"
kicad-pcb := "shield-pcb"

kicad-checks:
    kicad-cli pcb drc ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # kicad-cli sch check ergogen/schematic/ergogenesis.kicad_sch
    # kicad-cli pcb check ergogen/output/pcb/ergogenesis.kicad_pc

freerouting-gui:
    # nix-shell -p freerouting --run 'freerouting'
    nix shell nixpkgs#freerouting \
        --command freerouting \
        -de "./ergogen/output/pcbs/shield-pcb.dsn" \
        -do "./ergogen/output/pcbs/shield-pcb-routed.ses" \
        -di "./ergogen/output/pcbs/"
    # other cli args: https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md
    #  --gui.enabled=false
    # other settings: https://github.com/freerouting/freerouting/blob/master/docs/settings.md

    # has api server! use from Kicad?

pdf:
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
