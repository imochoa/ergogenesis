set positional-arguments := true

set shell := ["bash", "-euco", "pipefail"]


# draw := absolute_path('draw')
draw := justfile_directory()/'draw'
config := justfile_directory()/'config'

# \ls ./flake.nix |  entr -d -c just layout-img
[no-cd]
layout-img:
    nix build .#layoutImage
    rm -rf ./imgs
    mkdir -p ./imgs
    cp result/* imgs/
    chown -R "$USER" ./imgs/
    # not required! TODO: same for uf2 probably...
    # find ./result/ -type f -exec cp "$(readlink -f {})" ./imgs \;

# alias -g fullauto="find \$PWD -name '.*' -prune -o -print | entr zsh -c \"git commit -am 'auto' && git push\""

[no-cd]
local-layout:
    firefox "file://{{ justfile_directory() }}/sweep_keymap.ortho.svg"
    find "`pwd`/config/" -name '.*' -prune -o -print | entr -cd zsh -c 'pipx run keymap-drawer parse --columns 10 -z ./config/cradio.keymap > sweep_keymap.yaml && pipx run keymap-drawer draw sweep_keymap.yaml > sweep_keymap.ortho.svg'

[no-cd]
develop-layout:
    # @just layout-img
    firefox "file://{{ justfile_directory() }}/result/layout.svg"
    # fd -epdf . result/ | head -n1 | xargs xdg-open
    # TODO: send command to refresh firefox??
    find "`pwd`/config/" -name '.*' -prune -o -print | entr -cd zsh -c 'nix build .#layoutImage'
    # find "`pwd`/config/" -name '.*' -prune -o -print | entr -cd zsh -c 'nix build .#layoutImage && fd -epdf . result/ | head -n1 | xargs xdg-open'
    # \ls "config/" | entr -d nix build .#layoutImage

# parse & plot keymap
[no-cd]
draw:
    #!/usr/bin/env bash
    set -euo pipefail
    keymap -c "{{ draw }}/config.yaml" parse -z "{{ config }}/cradio.keymap" --virtual-layers Combos >"{{ draw }}/base.yaml"
    # yq -Yi '.combos.[].l = ["Combos"]' "{{ draw }}/base.yaml"
    keymap -c "{{ draw }}/config.yaml" draw "{{ draw }}/base.yaml" -k "ferris/sweep" >"{{ draw }}/base.svg"
