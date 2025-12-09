set positional-arguments := true
set shell := ["bash", "-euco", "pipefail"]

out := absolute_path( justfile_directory() + "/firmware")

_devc-check:
    #!/usr/bin/env bash
    if [ -z "$IS_DEVCONTAINER" ]; then
      printf "NOT in devc\n"
      exit 1
    fi

mkdirs: _devc-check
    mkdir -p "{{ justfile_directory() }}/modules"
    mkdir -p "{{ justfile_directory() }}/zmk"
    mkdir -p "{{ justfile_directory() }}/zephyr"
    mkdir -p "{{ justfile_directory() }}/.build"
    mkdir -p "{{ justfile_directory() }}/.tools"
    mkdir -p "{{ justfile_directory() }}/.home"
    cp -r /tmp/home-backup/* "{{ justfile_directory() }}/.home/"

    # .west should be made via the init recipe!
    # mkdir -p "{{ justfile_directory() }}/.west"
    #
    # TODO: copy .home to ~/home, then mount
    # in ~
    # .cache
    # .cmake

hard-rmdirs: _devc-check && mkdirs
    rm -rf "{{ justfile_directory() }}/modules"
    rm -rf "{{ justfile_directory() }}/zmk"
    rm -rf "{{ justfile_directory() }}/zephyr"
    rm -rf "{{ justfile_directory() }}/.build"
    rm -rf "{{ justfile_directory() }}/.tools"
    rm -rf "{{ justfile_directory() }}/.west"
    rm -rf "{{ justfile_directory() }}/.home"

# initialize west
west-init: hard-rmdirs
    west init -l config

# you might need to run this multiple times after "init"
west-update:
    west update --fetch-opt=--filter=blob:none
    west zephyr-export
    git config --global --add safe.directory "{{ justfile_directory() }}/zmk"
    git config --global --add safe.directory "{{ justfile_directory() }}/zephyr"

# update west
update: _devc-check 
    west update --fetch-opt=--filter=blob:none

# Builds with ZMK Studio
build-firmware shield="ergogenesis": _devc-check && _ls_out
    #!/usr/bin/env bash
    set -euxo pipefail
    # https://www.reddit.com/r/ErgoMechKeyboards/comments/1hkhyht/guide_building_zmk_firmware_locally_with_only_a/

    # that you may need to run west update a few times for everything to be fetched.
    # west init -l config && west update
    out="{{ out }}"

    mkdir -p "${out}"
    rm -rf "${out}/*.uf2"

    # says to call it from zmk/app...
    export Zephyr_DIR="{{ justfile_directory() }}/zephyr/share/zephyr-package/cmake"
    shield="{{ shield }}"

    # If you use a local development environment to build firmware instead of GitHub Actions, pass the -DSHIELD=settings_reset argument when building, omitting all other -DSHIELD arguments.

    for side in "left" "right"; do
      build="{{ justfile_directory() }}/.build/${side}"

      echo "${side}"
      echo "${build}"

      rm -rf "${build}"
      mkdir -p "${build}" 

      CMAKE_PREFIX_PATH="{{ justfile_directory() }}/zephyr:\$CMAKE_PREFIX_PATH" west build \
        --pristine \
        --build-dir "${build}" \
        --board "nice_nano_v2" \
        --snippet "studio-rpc-usb-uart" \
        "{{ justfile_directory() }}/zmk/app" \
        -- \
        -DZMK_CONFIG="{{ justfile_directory() }}/config" \
        -DSHIELD="${shield}_${side}" \
        -DCONFIG_ZMK_STUDIO="y"

      if [[ -f "${build}/zephyr/zmk.uf2" ]]; then
        cp "${build}/zephyr/zmk.uf2" "${out}/zmk_${side}.uf2"
      fi
    done

# https://zmk.dev/docs/troubleshooting/connection-issues#reset-split-keyboard-procedure
build-settings-reset-firmware: _devc-check && _ls_out
    #!/usr/bin/env bash
    set -euxo pipefail
    # https://www.reddit.com/r/ErgoMechKeyboards/comments/1hkhyht/guide_building_zmk_firmware_locally_with_only_a/

    # that you may need to run west update a few times for everything to be fetched.
    # west init -l config && west update
    out="{{ out }}"

    mkdir -p "${out}"

    # says to call it from zmk/app...
    export Zephyr_DIR="{{ justfile_directory() }}/zephyr/share/zephyr-package/cmake"

    # If you use a local development environment to build firmware instead of GitHub Actions, pass the -DSHIELD=settings_reset argument when building, omitting all other -DSHIELD arguments.
    build="{{ justfile_directory() }}/.build/settings_reset"

    echo "${build}"

    rm -rf "${build}"
    mkdir -p "${build}" 

    CMAKE_PREFIX_PATH="{{ justfile_directory() }}/zephyr:\$CMAKE_PREFIX_PATH" west build \
      --pristine \
      --build-dir "${build}" \
      --board "nice_nano_v2" \
      "{{ justfile_directory() }}/zmk/app" \
      -- \
      -DZMK_CONFIG="{{ justfile_directory() }}/config" \
      -DSHIELD="settings_reset"

    if [[ -f "${build}/zephyr/zmk.uf2" ]]; then
      cp "${build}/zephyr/zmk.uf2" "${out}/zmk_reset.uf2"
    fi

_ls_out:
    ls -la "{{ out }}"
