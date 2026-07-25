set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

# Sub-module of firmware/justfile. These recipes run INSIDE the devcontainer
# (container env var is set). justfile_dir() resolves to firmware/ since
# firmware/justfile is always invoked via `cd firmware && just`.

fw := justfile_dir()
out := fw

[no-cd]
[private]
_devc-check:
    #!/usr/bin/env bash
    if [ -z "${container}" ]; then
      printf "NOT in devc\n"
      exit 1
    fi

[no-cd]
mkdirs: _devc-check
    mkdir -p "{{ fw }}/modules"
    mkdir -p "{{ fw }}/zmk"
    mkdir -p "{{ fw }}/.build"
    mkdir -p "{{ fw }}/tools"

    # .west should be made via the init recipe!
    # mkdir -p "{{ fw }}/.west"

    # zephyr is a bind-mounted dir, so it already exists on the host.

[no-cd]
hard-rmdirs: _devc-check && mkdirs
    rm -rf "{{ fw }}/modules"
    rm -rf "{{ fw }}/zmk"
    rm -rf "{{ fw }}/.build"
    rm -rf "{{ fw }}/tools"
    rm -rf "{{ fw }}/.west"

    # zephyr is a bind mount (not a volume); only clear its contents.
    rm -rf "{{ fw }}/zephyr/"*

# initialize west
[group('west')]
[no-cd]
west-init:
    ( unset ZEPHYR_BASE && west init --local "{{ fw }}/config" )

[group('west')]
[no-cd]
west-reset: hard-rmdirs west-init

# you might need to run this multiple times after "init"
[group('west')]
[no-cd]
west-update:
    # The bind-mounted repos are owned by the host user (mapped to uid 1000
    # via keep-id), which git inside the container flags as "dubious
    # ownership". Exempt them *before* west update tries to touch the repos.
    git config --global --add safe.directory "{{ fw }}/zmk"
    git config --global --add safe.directory "{{ fw }}/zephyr"
    git config --global --add safe.directory "*"
    west update --fetch-opt=--filter=blob:none
    west zephyr-export

# Builds with ZMK Studio

# snippet/cmake_args may be empty; they are only forwarded when set.
[no-cd]
generic-build board shield snippet="" cmake_args="" artifact_name="": _devc-check && _ls_out
    #!/usr/bin/env bash
    set -euxo pipefail
    # https://www.reddit.com/r/ErgoMechKeyboards/comments/1hkhyht/guide_building_zmk_firmware_locally_with_only_a/

    # says to call it from zmk/app...
    out="{{ out }}"
    board="{{ board }}"
    shield="{{ shield }}"
    snippet="{{ snippet }}"
    cmake_args="{{ cmake_args }}"
    artifact_name="{{ artifact_name }}"
    artifact_name="${artifact_name:-${shield}-${board}-zmk}"

    # that you may need to run west update a few times for everything to be fetched.
    # west init -l config && west update
    mkdir -p "${out}"
    build="{{ fw }}/.build/${board}/${shield}"
    mkdir -p "${build}"

    export Zephyr_DIR="{{ fw }}/zephyr/share/zephyr-package/cmake"

    # If you use a local development environment to build firmware instead of GitHub Actions, pass the -DSHIELD=settings_reset argument when building, omitting all other -DSHIELD arguments.

    rm -rf "${build}"
    mkdir -p "${build}"

    # Only pass --snippet when a snippet is actually requested; an empty
    # --snippet makes west/cmake misparse the following positional args.
    snippet_flag=()
    if [[ -n "${snippet}" ]]; then
      snippet_flag=(--snippet "${snippet}")
    fi

    CMAKE_PREFIX_PATH="{{ fw }}/zephyr:\$CMAKE_PREFIX_PATH" west build \
      --pristine \
      --build-dir "${build}" \
      --board "${board}" \
      "${snippet_flag[@]}" \
      "{{ fw }}/zmk/app" \
      -- \
      -DZMK_CONFIG="{{ fw }}/config" \
      -DSHIELD="${shield}" \
      ${cmake_args}

    # TODO: technically also .bin files exist?
    if [[ -f "${build}/zephyr/zmk.uf2" ]]; then
      cp "${build}/zephyr/zmk.uf2" "${out}/${artifact_name}.uf2"
    fi

[no-cd]
_ls_out:
    ls -la "{{ out }}"
