set positional-arguments := true

set shell := ["bash", "-euco", "pipefail"]

# config := absolute_path('config')
# out := absolute_path('firmware')
# build := absolute_path('.build')
# result := absolute_path('result')
# draw := absolute_path('draw')
# home_dir := env('HOME')

output-dir := "{{justfile_dir()}}/ergogen/output"
pcb := "shield-pcb"

checks:
    k;icad-cli pcb drc ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # cli sch check ergogen/schematic/ergogenesis.kicad_sch
    # cli pcb check ergogen/output/pcb/ergogenesis.kicad_pc

freerouting-gui:
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

export-pdf:
    # front
    cli pcb export pdf \
        -l F.Cu,F.Adhesive,F.Paste,F.Silkscreen,F.Mask,F.Courtyard,F.Fab,Edge.Cuts \
        --output pcb-FRONT.pdf \
        --black-and-white \
        --include-border-title \
        ./ergogen/output/pcbs/shield-pcb.kicad_pcb
    # back
    cli pcb export pdf \
        -l B.Cu,B.Adhesive,B.Paste,B.Silkscreen,B.Mask,B.Courtyard,B.Fab,Edge.Cuts \
        --output pcb-BACK.pdf \
        --black-and-white \
        --include-border-title \
        ./ergogen/output/pcbs/shield-pcb.kicad_pcb
