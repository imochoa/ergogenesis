# overkeys/

An on-screen overlay of the ergogenesis keymap for macOS, using
[Coobaha's OverKeys fork](https://github.com/Coobaha/OverKeys). Modelled on
[mato1411/overkey-go60](https://github.com/mato1411/overkey-go60).

## Usage

```bash
just overkeys convert         # write output/overkeys_config.json
just overkeys install-config  # convert, then copy it into OverKeys
just overkeys app-install     # clone, build and install the app (Flutter + Xcode)
just overkeys enable-user-layouts  # one-time: make OverKeys use the config
just overkeys all             # app-install + install-config + enable-user-layouts
```

After a later `install-config`, pick **Reload config** in the OverKeys tray
menu. `enable-user-layouts` sets **Enable advanced settings** and **Use user
layouts** (Preferences > General) and restarts the app; without them OverKeys
shows a standard keyboard. The app needs Accessibility and Input Monitoring
permission. It stays on screen by default; auto-hide is in its preferences.

`app-build` applies `app.patch` to the pinned checkout and builds for the host
architecture only, which is what current macOS and Xcode need.

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

The trigger is **off by default** and has not been tested on hardware yet
(TODO). Enable it by building the left (central) half with
`just firmware build-firmware-overkeys` and flashing it; `build-firmware`
builds the plain variant again. Without it the overlay still shows the layout
and highlights keys, but stays on the base layer.

To add one, define another `OVK_*` key and `mo_*` macro in the keymap, use it
as the hold binding of that layer's hold-tap, and add the layer to `TRIGGERS`
in `convert.py`. Then rebuild and flash the firmware.

- The trigger must be one of F13-F20. USB HID defines F1-F24 only (there is
  no F25 or F32), and macOS only reports F1-F20.
- Layers without a trigger are still in the config and can be selected from the
  OverKeys tray menu.


### Side effects of the trigger key

The trigger is an ordinary key press, so every application receives it, not
only OverKeys. None of this has been observed on hardware yet (TODO).

- **Shortcuts still work.** Holding Ctrl and pressing `+` on the Symbols layer
  sends Ctrl, F20, then `+`. F20 is not a modifier, so the application still
  sees Ctrl-`+`. ZMK combos are resolved in the keyboard and are unaffected.
- **A stray F20 on every hold.** If a modifier is already down when the layer
  key is pressed, the host sees that modifier with F20 (for example Ctrl-F20).
  Anything bound to F20, with or without modifiers, will fire.
- **Terminals get F20 as input.** A terminal turns it into an escape sequence
  for the shell, vim or tmux. Unmapped, it may print stray characters or cancel
  a pending vim command. Map F20 to a no-op there if this happens.
- **Shortcut recorders** may capture F20 instead of the intended keys.
- **Key repeat.** F20 auto-repeats while it is the only key held, so the
  effects above can repeat until another key is pressed.

Any trigger key behaves this way. Leaving the indicator off (the default)
avoids all of it.
