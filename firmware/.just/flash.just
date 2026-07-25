set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

# Flash recipes (run on the host, not in the devcontainer).
# .uf2 files are built into firmware/ by the build recipes.

fw := justfile_dir()
out := fw

# Reset both halves.
[no-cd]
reset-firmware: (_flash_one "settings_reset-nice_nano_v2-zmk.uf2") (_flash_one "settings_reset-nice_nano_v2-zmk.uf2")

# Flash left then right.
[no-cd]
firmware: (_flash_one "ergogenesis_left-nice_nano_v2-zmk.uf2") (_flash_one "ergogenesis_right-nice_nano_v2-zmk.uf2")

[no-cd]
_flash_one firmware:
    #!/usr/bin/env bash
    set -euxo pipefail

    firmware="{{ firmware }}"

    tmpdir=$(mktemp -d)
    trap 'popd && rm -rf "${tmpdir}"' EXIT
    pushd "${tmpdir}" > /dev/null
    # timestamp file
    ts="${tmpdir}/ts"

    # ref: https://github.com/lilyinstarlight/zmk-nix/blob/f02a78c8c06d283ea1399c14aaec308bfb77dc1b/nix/flash.nix#L8
    # TODO: check for darwin
    # kb_dir="/media/$USER"
    kb_dir="/Volumes/"

    uf2="{{ out }}/${firmware}"
    [ ! -f "${uf2}" ] && exit 1

    printf "Bootloader ${firmware}\n"
    rm -rf "${ts}" && touch "${ts}"
    res=""
    while [[ -z ${res} ]]; do
      printf "."
      sleep 1
      res=$(find "${kb_dir}" -mindepth 1 -maxdepth 1 -type d  -newer "${ts}");
    done
    bl_dir=$(head -n 1 <<< "${res}" )
    : sudo is required in macOS to not get a permission error copying to the removable drive...
    : could not copy extended attributes permission denied, use rsync
    sudo rsync -azP --no-owner --no-group "${uf2}" "${bl_dir}/"
