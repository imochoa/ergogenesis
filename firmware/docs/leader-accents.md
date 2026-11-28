# Accented characters with the leader key

The keymap types `ñ`, the German umlauts and the Spanish accents through a
leader key: press the leader, then a short key sequence, and the keyboard
sends the character.

## Typing

Press **W+E together** (base layer) to start a sequence, release, then type:

| Sequence   | Output | With Shift held |
| ---------- | ------ | --------------- |
| `A`        | ä      | Ä               |
| `O`        | ö      | Ö               |
| `U`        | ü      | Ü               |
| `S`        | ß      | ẞ               |
| `N`        | ñ      | Ñ               |
| `E` `A`    | á      | Á               |
| `E` `E`    | é      | É               |
| `E` `I`    | í      | Í               |
| `E` `O`    | ó      | Ó               |
| `E` `U`    | ú      | Ú               |
| `/`        | ¿      |                 |
| `E` `/`    | ¡      |                 |
| `C`        | €      |                 |
| `M` `A` `C` | switch to macOS input |  |
| `L` `I` `N` | switch to Linux input |  |

- There is no timeout. A key that matches no sequence cancels the leader and
  is typed normally.
- For a capital, hold Shift with the opposite hand while typing the last key.
- The W+E combo is ignored within 150 ms of another key press, so that typing
  "we" does not trigger it. Pause briefly before pressing it mid-word.

## Host setup

The characters are sent as Unicode code points
([zmk-unicode](https://github.com/urob/zmk-unicode)), which the host has to
accept. The keyboard cannot detect the host, so it has one active input system
at a time. It starts in macOS mode after power-up (`default-mode` in the
keymap).

- **macOS**: System Settings → Keyboard → Input Sources → add *Unicode Hex
  Input* (under *Other*) and select it. While it is selected, Option-based
  shortcuts such as Option+Left/Right may stop working.
- **Linux**: works out of the box where IBus is running (GNOME) and in GTK
  apps, through `Ctrl+Shift+U`. Elsewhere it may not work. Switch the keyboard
  with leader `L` `I` `N` first.

If output looks mangled (wrong or missing characters), raise
`CONFIG_ZMK_UNICODE_TAP_MS` / `CONFIG_ZMK_UNICODE_WAIT_MS` in
`config/ergogenesis.conf`.

## Changing the output backend

The sequences bind to `CH_*` aliases defined at the top of
`config/ergogenesis.keymap`. To stop depending on Unicode input, repoint the
aliases, for example at the AltGr positions of a host layout such as EurKEY
(`#define CH_DE_AE &kp RA(A)`); the sequences stay unchanged.

## Adding a sequence

Add a child node to the `leader` behavior in the keymap. Sequences are
keycode-based and must be prefix-free: `A` and `A E` cannot both exist. The
defaults allow 32 sequences of up to 5 keys
(`CONFIG_ZMK_LEADER_MAX_SEQUENCES`, `CONFIG_ZMK_LEADER_MAX_KEYS_PER_SEQUENCE`).
