 The new global-quick-tap-ms = <75>; settings makes it so that if any key was pressed within 75ms before the combo hit, the combo won't be run and instead the keys will register as taps.

This significantly reduces accidental activations during typing and made combos finally usable for me.

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

## Keymap Drawing

https://github.com/infused-kim/zmk-config/blob/chocofi/main/keymap_img/keymap_img_adjuster.py

```
echo 'Parsing ZMK keymap...'
keymap -c keymap_config.yaml parse -c 12 -z ../config/corne.keymap > keymap.yaml

# echo '\n\nAdjusting keymap yaml...'
# ./keymap_img_adjuster.py keymap.yaml

echo '\n\nDrawing keymap...'
keymap -c keymap_config.yaml draw --qmk-keyboard crkbd/rev1 --qmk-layout LAYOUT_split_3x6_3 keymap.yaml -s Base Nav Num Func Sym Adjust > keymap.svg
```


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
