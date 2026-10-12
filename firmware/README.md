 The new global-quick-tap-ms = <75>; settings makes it so that if any key was pressed within 75ms before the combo hit, the combo won't be run and instead the keys will register as taps.

This significantly reduces accidental activations during typing and made combos finally usable for me.

## Flashing split firmware

The **left half is the central** and the right half is the peripheral. For most
keymap-only changes, flashing the left half is enough because the central
resolves key positions into key bindings and behaviors.

| Change | Half to flash |
| --- | --- |
| Keymap bindings, layers, combos, macros, or hold-tap timings in `config/ergogenesis.keymap` | Left/central only |
| Left-specific overlay, GPIO, or scanning changes | Left only |
| Right-specific overlay, GPIO, or scanning changes | Right only |
| Shared shield hardware, split transport, Kconfig, ZMK/Zephyr version, or module changes | Both halves |
| Clear broken split pairing or all persistent settings | Settings-reset image on both halves, then normal firmware on both halves |
| Unsure whether code runs on the peripheral | Both halves |

### When to use the settings-reset firmware

A routine firmware update does **not** require flashing
`outputs/settings_reset-nice_nano-zmk.uf2` first. Regular firmware preserves
Bluetooth bonds and other persistent settings by design.

Use the settings-reset image only for a full settings reset, such as when:

- the two halves no longer pair with each other;
- changing which half is the central, replacing a controller, or reusing a
  controller from another split leaves stale split bonds;
- stale host bonds cannot be cleared with the keymap's Bluetooth-clear behavior;
  or
- deliberately erasing all saved settings, including Bluetooth profiles, output
  selection, and ZMK Studio changes.

The reset image erases the settings partition and cannot operate as the normal
keyboard firmware. Reset and restore the keyboard in this order:

1. Build it with `just build-settings-reset-firmware` (or as part of
   `just build-all`).
2. Flash `outputs/settings_reset-nice_nano-zmk.uf2` to **both halves**.
3. Flash `outputs/ergogenesis_left-nice_nano-zmk.uf2` to the left half and
   `outputs/ergogenesis_right-nice_nano-zmk.uf2` to the right half.
4. Forget Ergogenesis on each previously paired host, then pair it again.

The flash recipes perform steps 2 and 3 as `just flash reset-firmware` followed
by `just flash firmware`. From the repository root, prefix those commands with
`just firmware`.

## Battery sensing and Pro Micro pin 21

Do not configure the SuperMini battery sensor on AIN7 / P0.31. The `nice_nano`
board maps that GPIO to Pro Micro pin 21, and this keyboard already uses pin 21
as a direct key input:

- left half: `middle_home` (`D` on the base layer)
- right half: `inner_top` (`Y` on the base layer)

A `zmk,battery-voltage-divider` node using `io-channels = <&adc 7>` takes over
P0.31 and stops both keys from scanning. Battery ADC sensing and split battery
proxying therefore stay disabled in `config/ergogenesis.conf` and
`config/boards/shields/ergogenesis/Kconfig.defconfig`. Re-route those keys or
use a different battery-sense GPIO before enabling battery measurement.

## Keymap drawing

Generate the tracked layout artifacts from the repository root:

```bash
just firmware draw draw-pdf
```

This updates `outputs/base.svg` and `outputs/base.pdf`. The parsed intermediate
layout remains in `draw/base.yaml`.

## External modules (urob)

Two [urob](https://github.com/urob) ZMK modules are pinned in
[`config/west.yml`](config/west.yml). Both track ZMK `main` (their `main`
branch) — the `v0.3` in their READMEs is a "match your ZMK release" convention,
not a floor — so they build against this repo's ZMK-main pin. Bump the SHAs in
`west.yml` to move forward, then re-run `just firmware west-update` + a pristine
build.

- **[zmk-unicode](https://github.com/urob/zmk-unicode)** — Unicode input via the
  `&uc` behavior. Type code points directly (`&uc 0xE4 0xC4` → `ä`/`Ä`) or with
  language macros (`&uc UC_DE_AE`). Supports six input systems (macOS, Linux,
  Linux-alt, WinCompose, Windows-Alt, Emacs) with **runtime switching** — the
  keymap sets a boot default via `UC_DEFAULT` / `default-mode` and the
  `&uc UC_SET_MACOS` / `&uc UC_SET_LINUX` keys on the `LY_CTL` layer flip it
  live (no host-OS auto-detection exists in ZMK; this is the switch). macOS
  needs the "Unicode Hex Input" keyboard enabled.

- **[zmk-helpers](https://github.com/urob/zmk-helpers)** — convenience macros for
  terser keymaps: `ZMK_COMBO`, `ZMK_MACRO`, `ZMK_HOLD_TAP`, `ZMK_MOD_MORPH`,
  `ZMK_LAYER`, and standardized key-position labels (`LT0`…`RH2`, `KEYS_L`,
  `KEYS_R`, `THUMBS`). Included via `#include "zmk-helpers/helper.h"`. The custom
  shield keeps a local snapshot of the module's standard `36.h` position labels
  so it remains self-contained. The module's `unicode-chars/*.dtsi` are
  deprecated in favor of the zmk-unicode module above.
