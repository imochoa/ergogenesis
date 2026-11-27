# overkeys/

An on-screen overlay of the ergogenesis keymap for macOS, using
[Coobaha's OverKeys fork](https://github.com/Coobaha/OverKeys). Modelled on
[mato1411/overkey-go60](https://github.com/mato1411/overkey-go60).

## Usage

```bash
just overkeys convert         # write output/overkeys_config.json
just overkeys install-config  # convert, then copy it into OverKeys
just overkeys app-install     # clone, build and install the app (Flutter + Xcode)
just overkeys all             # app-install + install-config
```

After `install-config`, pick **Reload config** in the OverKeys tray menu. In
Preferences > General, turn on **Enable advanced settings** and **Use user
layouts** once. The app needs Accessibility and Input Monitoring permission.

## How it works

`convert.py` builds the config from two sources, so nothing is duplicated here:

- **Labels**: keymap-drawer's parse of `firmware/config/ergogenesis.keymap`,
  using `firmware/draw/config.yaml`. One OverKeys layout per ZMK layer.
- **Key positions**: the `zmk,physical-layout` node in
  `firmware/config/boards/shields/ergogenesis/ergogenesis.dtsi`.

## Layer triggers

OverKeys cannot see ZMK layers. The firmware therefore holds a trigger key for
as long as a layer is active, and the config maps that key to a layout.

| Layer   | Trigger | Keymap behaviour         |
| ------- | ------- | ------------------------ |
| Symbols | F20     | `&lt_sym` via `&mo_sym`  |

To add one, define another `OVK_*` key and `mo_*` macro in the keymap, use it
as the hold binding of that layer's hold-tap, and add the layer to `TRIGGERS`
in `convert.py`. Then rebuild and flash the firmware.

- macOS only reports F1-F20, so F21-F24 cannot be triggers.
- The host receives the trigger key too. Pick keys with no shortcut bound.
- Layers without a trigger are still in the config and can be selected from the
  OverKeys tray menu.
