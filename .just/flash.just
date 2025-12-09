set positional-arguments := true

set shell := ["bash", "-euco", "pipefail"]


out := justfile_directory() + "/firmware"
# out := absolute_path( justfile_directory() + "/firmware")

[no-cd]
reset-firmware: (_flash "zmk_reset.uf2" "zmk_reset.uf2")

[no-cd]
firmware: (_flash "zmk_left.uf2" "zmk_right.uf2")

[no-cd]
_flash fm_left fm_right:
  #!/usr/bin/env bash
  # set -euxo pipefail
  tmpdir=$(mktemp -d)
  trap 'popd && rm -rf "${tmpdir}"' EXIT
  pushd "${tmpdir}" > /dev/null
  # timestamp file
  ts="${tmpdir}/ts"

  # ref: https://github.com/lilyinstarlight/zmk-nix/blob/f02a78c8c06d283ea1399c14aaec308bfb77dc1b/nix/flash.nix#L8
  # TODO: check for darwin
  # kb_dir="/media/$USER"
  kb_dir="/Volumes/"

  printf "Flash left and then right\n"

  for f in "{{fm_left}}" "{{fm_right}}";
  do
    uf2="{{ out }}/${f}"
    [ ! -f "${uf2}" ] && exit 1

    printf "Bootloader ${f}\n"
    rm -rf "${ts}" && touch "${ts}"
    res=""
    while [[ -z ${res} ]]; do
      printf "."
      sleep 1
      res=$(find "${kb_dir}" -type d -maxdepth 1 -depth 1 -newer "${ts}");
    done
    bl_dir=$(head -n 1 <<< "${res}" )
    : sudo is required in macOS to not get a permission error copying to the removable drive...
    : could not copy extended attributes permission denied, use rsync
    # cp --no-preserve=xattr source 1 2
    sudo rsync -azP --no-owner --no-group "${uf2}" "${bl_dir}/"
  done
