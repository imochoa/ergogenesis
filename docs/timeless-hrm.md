# Timeless home-row mods alignment

Both keyboard configurations now follow the Timeless home-row-mod setup from
[urob/zmk-config](https://github.com/urob/zmk-config).

## Previous differences

Both configurations already used the core Timeless HRM mechanics:

- ZMK's `balanced` hold-tap flavor
- separate left- and right-hand HRM behaviors
- positional hold-taps
- `hold-trigger-on-release`

They differed from urob's configuration in these details:

| Setting | Previous | Aligned |
| --- | ---: | ---: |
| `tapping-term-ms` | 220 ms | 280 ms |
| `quick-tap-ms` | 150 ms | 175 ms |
| `require-prior-idle-ms` | 100 ms | 150 ms |

The positional trigger lists also included same-hand HRM positions:

```dts
hold-trigger-key-positions = <KEYS_R THUMBS KEYS_HRM_L>;
hold-trigger-key-positions = <KEYS_L THUMBS KEYS_HRM_R>;
```

They now match urob's opposite-hand-plus-thumbs configuration:

```dts
hold-trigger-key-positions = <KEYS_R THUMBS>;
hold-trigger-key-positions = <KEYS_L THUMBS>;
```

Ergogenesis's `THUMBS` definition previously omitted its two outer thumb keys.
It now includes all six thumb positions. The Ferris Sweep already included all
four of its thumb positions. Both position-label headers now provide urob's
standard `THUMBS_L`, `THUMBS_R`, and `THUMBS` definitions.

## Files changed

### Ergogenesis

- `ergogenesis/firmware/config/ergogenesis.keymap`
- `ergogenesis/firmware/config/boards/shields/ergogenesis/ergogenesis.keymap`
- `ergogenesis/firmware/config/boards/shields/ergogenesis/36.h`
- `ergogenesis/firmware/README.md`

### Ferris Sweep

- `ferris-sweep-zmk-nix/config/cradio.keymap`
- `ferris-sweep-zmk-nix/config/34.h`

## Validation

- A full left-side Ergogenesis Studio firmware build passed.
- Ferris Sweep CMake and devicetree generation passed against the same pinned
  ZMK version. The generated devicetree confirmed the 280/175/150 ms settings
  and the corrected positional trigger lists.
- A full standalone Ferris Sweep build was not completed because its fresh
  `west update` exceeded the validation timeout.
- `git diff --check` passed in both repositories.

## Unchanged generic hold-tap

The separate generic `&ht` behavior still uses 220/150/100 ms. It is not used by
the home-row mods, so it was intentionally left unchanged.
