# AGENTS.md — firmware/

ZMK firmware for the ergogenesis keyboard. Built inside a podman devcontainer
(the same pattern as `ferris-sweep-zmk-nix2`).

## Layout

```
firmware/
├── config/                 ZMK keymap + board/shield definitions (the west manifest root)
│   ├── west.yml            west manifest (pins ZMK main @ a fixed commit → Zephyr 4.1)
│   ├── ergogenesis.conf    board-level Kconfig config
│   └── boards/shields/ergogenesis/
│       ├── ergogenesis.dtsi     kscan GPIO mapping + matrix transform (THE pin map)
│       ├── ergogenesis.keymap   keymap layers + combos + behaviors
│       ├── ergogenesis_left.overlay / _right.overlay   per-half overlays
│       ├── 36.h                 key-position label macros (LT0..RH2)
│       ├── helper.h             combo/macro helper macros
│       └── Kconfig.defconfig    ZMK split / central role config
├── .devcontainer/          podman devcontainer (Dockerfile, devcontainer.json, scripts)
│   └── home/               bind-mounted $HOME for the container (gitignored)
├── .just/
│   ├── in-devc.just        recipes that run INSIDE the container (west, build)
│   ├── flash.just          recipes that flash .uf2 files to the MCU (host-side)
│   └── draw.just           keymap-drawer recipes (SVG/PDF layout rendering)
├── draw/                   keymap layout rendering config + output (SVG, PDF, YAML)
├── justfile                firmware recipes (run via `just firmware <recipe>` from root)
├── flake.nix               nix dev shell (Zephyr SDK + toolchain) — NOT used by the devcontainer
├── .envrc                  direnv entry point for the nix shell
├── script.sh               old standalone build script (reference only)
├── zmk/                    west-managed ZMK source (gitignored, ~21 entries)
├── zephyr/                 west-managed Zephyr source (gitignored, ~45 entries)
├── modules/                west-managed HAL modules (gitignored, ~37 repos)
├── .build/                 CMake/Ninja build output (gitignored)
├── .west/                  west workspace metadata
├── tools/                  west-managed tools (gitignored)
└── *.uf2                   built firmware outputs (gitignored)
```

## Building

All builds run inside the podman devcontainer. From the repo root:

```bash
just firmware devc-up              # start the devcontainer (builds image if needed)
just firmware west-init            # one-time: west init --local config
just firmware west-update          # one-time (slow): clones zmk + zephyr + ~37 modules
just firmware build-all            # build left + right + settings_reset .uf2 files
# or individually:
just firmware build-firmware       # left + right (with ZMK Studio)
just firmware build-settings-reset-firmware
```

`generic-build` is **incremental by default** (reuses the build dir — seconds for
keymap/overlay edits). `build-all` / `build-firmware` / `build-settings-reset-firmware`
force a clean `--pristine` rebuild; pass a non-empty 6th arg to `generic-build`
for a one-off pristine build. Re-run pristine after changing `.conf`, `west.yml`,
`-D` flags, or the board/snippet.

For a custom build with empty snippet/cmake_args (e.g. settings_reset), call
directly from `firmware/` so empty-string args survive:

```bash
cd firmware && just generic-build nice_nano settings_reset "" "" settings_reset-nice_nano-zmk
```

## How the devcontainer works (macOS podman)

- `--userns=keep-id:uid=1000,gid=1000` maps the container's uid 1000 to the host
  user (macOS uid 501), so the bind-mounted workspace is writable.
- Named podman volumes are NOT used — on macOS they end up owned by an unmapped
  uid (999) that the container can't write to. Everything is a bind mount to
  project-local dirs instead.
- `.bashrc` lives inside the `home/` bind mount (a separate single-file bind on
  top of a dir bind trips crun on macOS podman).
- `west-update` sets `git config --global safe.directory` *before* `west update`
  because the bind-mounted repos are owned by the host user, which git inside
  the container flags as "dubious ownership".
- The `container=podman` env var is set in `devcontainer.json` so `devc-exec`
  knows it's inside the container (skips re-creating it).

## ZMK main / Zephyr 4.1 + HWMv2 `nice_nano` gotchas

Board is **`nice_nano`** (NOT `nice_nano_v2` — renamed in Hardware Model v2; the
old name errors). The HWMv2 board defconfig is minimal and DROPS several defaults
the old `nice_nano_v2` board provided, so `config/ergogenesis.conf` sets them
explicitly (each learned the hard way this migration):

- `CONFIG_ZMK_BLE=y` — else the build is USB-only and never advertises over BLE.
- `CONFIG_FLASH=y` + `CONFIG_FLASH_MAP=y` + `CONFIG_NVS=y` + `CONFIG_SETTINGS_NVS=y`
  — the settings/NVS storage backend. Without it `CONFIG_BT_SETTINGS` has nowhere
  to persist, so the keyboard forgets its pairing on every power cycle.
- `CONFIG_BT_SMP_ALLOW_UNAUTH_OVERWRITE=y` + `CONFIG_ZMK_BLE_PASSKEY_ENTRY=n`
  — Just Works pairing (no PIN) that overwrites a stale bond on re-pair. (The
  overwrite flag `imply`s passkey entry, hence the explicit `=n`.)
- `config/settings_reset.conf` re-adds the FLASH/NVS backend so the built-in
  `settings_reset` image can actually erase bonds (it relies on the board for
  storage, which HWMv2 no longer provides — otherwise it's a silent no-op).
- `config/west.yml` sets `group-filter: [-optional]` to stop west fetching
  Zephyr's optional modules (tflite-micro, thrift) into `optional/`.
- `.just/in-devc.just`: `west-update` no longer runs `west zephyr-export` (fails
  with a `zcmake` import error on the 4.1 image and isn't needed — `generic-build`
  passes `Zephyr_DIR` explicitly). `hard-rmdirs` fully wipes `zephyr/` including
  `.git` (a leftover `.git` leaves the 3.5→4.1 checkout half-populated) and
  removes `optional/`.

## Pin mapping (kscan ↔ physical keys)

`config/boards/shields/ergogenesis/ergogenesis.dtsi` defines the kscan
`input-gpios` order and the matrix-transform `map`. The GPIO index order MUST
match the physical key layout the transform expects (pinky→inner, top→bottom,
then thumbs). Each GPIO line is annotated with its ergogen key name for
traceability.

Pin → key assignments come from `hardware/ergogen/config.yaml` (the
`mcu-fp.Pxx:` lines). If you re-route the PCB, update the `Pxx:` assignments
there, then regenerate the PCB, then update the kscan `input-gpios` order in
`ergogenesis.dtsi` to match.

IMPORTANT: this is a reversible PCB with a reverse-mounted MCU, so the RIGHT
half's pins land on DIFFERENT physical keys than the left (a full permutation,
not a clean mirror). The right half therefore defines its OWN `input-gpios` in
`ergogenesis_right.overlay`; the shared transform + `col-offset = 18` then map
both halves correctly. `ergogenesis.dtsi` also defines a 36-key
`zmk,physical-layout` (required for ZMK Studio on this 3+3-thumb board).

`pro_micro N` in the dtsi refers to Arduino Pro Micro pin numbers (D0-D21),
which the `nice_nano` board maps to nRF52840 GPIOs. On the current HWMv2 board
those definitions live under `zmk/app/module/boards/nicekeyboards/nice_nano/`
(the old `boards/arm/nice_nano/` path is gone).

## Conventions

- The `.uf2` files are gitignored. Run `just firmware build-all` to (re)generate.
- `zmk/`, `zephyr/`, `modules/`, `optional/`, `.build/`, `.west/`, `tools/` are all
  gitignored (west-managed or build artifacts).
- The nix flake (`flake.nix`) provides a local Zephyr toolchain for non-devcontainer
  builds but is not the primary path. The devcontainer is.
- Do not hand-edit `zmk/`, `zephyr/`, or `modules/` — they are west-managed.
