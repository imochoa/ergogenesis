# ZMK timing debugging notes

Last updated: 2026-10-13

## Context

Repository: `~/Code/ergogenesis`

Active keymap source:

```text
firmware/config/ergogenesis.keymap
```

This file overrides the copy under `config/boards/shields/ergogenesis/`.
The keyboard is a split ZMK board with the **left half as central**. Keymap and
hold-tap decisions happen on the central, so timing-only changes require
flashing only the left half.

These issues became more noticeable after switching to lighter Choc switches.
The output patterns were consistent with hold-tap classification problems, not
switch chatter:

- `ai` instead of Shift+I
- `kv` instead of Ctrl+V
- Space disappearing when the next letter was pressed quickly

## Relevant ZMK concepts

### `require-prior-idle-ms`

Looks **backward** at the key pressed before the hold-tap. If another
non-modifier key was pressed within this interval, the hold-tap is forced to be
a tap.

- A larger value prevents accidental holds while typing.
- A larger value also makes intentional modifiers harder to invoke immediately
  after another key.
- This was the main cause of Shift-on-A failing immediately after Space.

### `tapping-term-ms`

The duration after which holding a hold-tap key by itself resolves as a hold.
It is not necessarily the delay for every chord: interrupt flavors may resolve
the decision earlier.

For the home-row mods, `balanced` can resolve a cross-hand chord before the
280 ms term when the other key is pressed and released while the home-row key
remains held.

### `quick-tap-ms`

If the same hold-tap key is pressed again within this interval, the second press
is forced to be a tap. This is useful for tap-then-hold key repetition. It was
not the primary cause of the problems in this session.

### Interrupt flavors

- `hold-preferred`: another key press immediately resolves the hold-tap as a
  hold. Responsive for layers, but dangerous for Space because rolling into the
  next letter can swallow the Space.
- `balanced`: another key must be pressed and released while the hold-tap is
  still held. Used for the home-row mods.
- `tap-preferred`: another key does not force a hold during the tapping term.
  Used for Space so fast typing cannot turn Space into a layer hold.

ZMK reference:
<https://zmk.dev/docs/keymaps/behaviors/hold-tap>

## Iteration history

### Initial timeless home-row settings

Both hands started with:

```dts
flavor = "balanced";
tapping-term-ms = <280>;
quick-tap-ms = <175>;
require-prior-idle-ms = <150>;
```

At 150 ms, intentional modifiers were frequently forced to taps. Typical
failures were `ai` instead of Shift+I and `kv` instead of Ctrl+V.

### First home-row adjustment: 150 ms to 100 ms

Both hands were changed to `require-prior-idle-ms = <100>`. This was noticeably
better with the lighter switches.

### Thumb experiment

The stock `&lt` behavior had been overridden globally with
`flavor = "hold-preferred"` to make the Symbols+Numbers tri-layer chord resolve
without waiting. A prior-idle guard was tested first at 75 ms and then 100 ms.

This did not fully solve swallowed spaces because `require-prior-idle-ms` only
examines the key **before** Space. With `hold-preferred`, the key pressed after
Space could still immediately turn Space into the Numbers-layer hold.

### Current split thumb behaviors

Space/Numbers now has a separate `tap-preferred` behavior. Symbols/Backspace
keeps the responsive global `&lt` behavior.

### Current left-hand adjustment

Because capital `I` is normally typed immediately after Space, the left-hand
home-row prior-idle value was reduced from 100 ms to 75 ms. The right hand
remains at 100 ms.

## Current configuration

At the end of this session, the effective timing configuration is:

```dts
/* Left-hand home-row mods: A/Shift, S/Alt, D/Ctrl, F/GUI. */
hml: hml {
    compatible = "zmk,behavior-hold-tap";
    #binding-cells = <2>;
    flavor = "balanced";
    tapping-term-ms = <280>;
    quick-tap-ms = <175>;
    require-prior-idle-ms = <75>;
    bindings = <&kp>, <&kp>;
    hold-trigger-key-positions = <KEYS_R THUMBS>;
    hold-trigger-on-release;
};

/* Right-hand home-row mods: J/GUI, K/Ctrl, L/Alt, ;/Shift. */
hmr: hmr {
    compatible = "zmk,behavior-hold-tap";
    #binding-cells = <2>;
    flavor = "balanced";
    tapping-term-ms = <280>;
    quick-tap-ms = <175>;
    require-prior-idle-ms = <100>;
    bindings = <&kp>, <&kp>;
    hold-trigger-key-positions = <KEYS_L THUMBS>;
    hold-trigger-on-release;
};

/* Space/Numbers: protect Space from being swallowed by the next letter. */
lt_num: layer_tap_number {
    compatible = "zmk,behavior-hold-tap";
    #binding-cells = <2>;
    flavor = "tap-preferred";
    tapping-term-ms = <200>;
    bindings = <&mo>, <&kp>;
};
```

The base-layer thumb binding is:

```dts
&lt_num LY_NUM SPACE
```

Symbols/Backspace still uses:

```dts
&lt LY_SYM BKSP
```

with the global override:

```dts
&lt {
    flavor = "hold-preferred";
    require-prior-idle-ms = <100>;
};
```

## Why the home-row tapping term is 280 ms

The 280 ms value is a fallback hold threshold and part of the standard timeless
home-row-mod setup. It does **not** mean that every Shift+I chord waits 280 ms.
With the balanced flavor, an opposite-hand key pressed and released while the
home-row modifier remains held can resolve the modifier earlier.

The long term helps avoid accidental holds and permits deliberate same-hand
modifier use. Shortening it may help if the modifier is held long enough to
cross the new threshold, but it does not fix a very short chord where the
home-row key is released before the target key.

## What to test now

After flashing the current left firmware, test these separately:

1. Type normal prose quickly and watch for missing spaces.
2. Repeatedly type capital `I` after Space.
3. Try Shift+I after pausing for at least half a second before pressing A/Shift.
4. Try Ctrl+V using K/Ctrl after both a pause and continuous typing.
5. Hold Space deliberately, wait for the Numbers layer, and type numbers.
6. Confirm that Backspace and the Symbols layer still feel responsive.

The pause test distinguishes two home-row failure modes:

- Works after a pause but fails after Space: `require-prior-idle-ms` is probably
  still too high.
- Fails even after a pause: likely balanced-flavor release order. Ensure the
  target key is released before releasing the home-row modifier.

## Possible next adjustments

Change one setting at a time.

### If Space is reliable but Numbers feels too slow

Reduce the Space/Numbers tapping term gradually:

```text
200 -> 175 -> 150 ms
```

Risk: a slightly long Space press can become the Numbers-layer hold.

### If Space is still swallowed

The `tap-preferred` Space behavior should prevent a following letter from
forcing a hold during the tapping term. Verify that the new left firmware was
actually flashed and that the effective devicetree contains `lt_num`.

If the behavior is present but the symptom remains, capture the exact key press
and release order before changing more timings.

### If `ai` still occurs only immediately after Space

Try reducing the left-hand prior-idle value:

```text
75 -> 50 ms
```

Risk: left-hand home-row keys become more likely to resolve as modifiers during
fast typing.

### If `ai` also occurs after a deliberate pause

Lowering prior-idle will not help. Investigate release order under the balanced
flavor. Possible experiments are:

1. Reduce the home-row tapping term from 280 to about 220 ms.
2. Define a Shift-specific behavior rather than changing all home-row mods.
3. Test `hold-preferred` for Shift only, understanding that intended cross-hand
   letter rolls such as literal `ai` may then become false Shift chords.

### If `kv` still replaces Ctrl+V

The right hand currently remains at 100 ms. Try reducing only `hmr` to 75 ms
before changing its tapping term.

### If Backspace is swallowed before a correction letter

Give Symbols/Backspace its own behavior too. Consider `balanced` or
`tap-preferred` instead of the current global hold-preferred `&lt` behavior.

## Build and flash

Build only the left/central firmware for timing and keymap changes:

```bash
cd ~/Code/ergogenesis/firmware
just generic-build \
  nice_nano \
  ergogenesis_left \
  studio-rpc-usb-uart \
  '-DCONFIG_ZMK_STUDIO=y' \
  ergogenesis_left-nice_nano-zmk
```

Current artifact location:

```text
~/Code/ergogenesis/firmware/outputs/ergogenesis_left-nice_nano-zmk.uf2
```

Flash only the left/central half for keymap, behavior, combo, macro, layer, and
timing changes. Flash both halves for shared hardware, split transport,
Kconfig, ZMK/Zephyr version, or module changes.

A normal timing update does not require the settings-reset UF2. Use settings
reset only to intentionally clear Bluetooth bonds or persistent settings.

## Verify the generated behavior

After building, inspect the effective devicetree:

```bash
cd ~/Code/ergogenesis/firmware
rg -n -A10 \
  'hml: hml|hmr: hmr|lt_num: layer_tap_number|lt: layer_tap' \
  .build/nice_nano/ergogenesis_left/zephyr/zephyr.dts
```

Hex values seen for the current timings:

```text
75 ms  = 0x4b
100 ms = 0x64
200 ms = 0xc8
280 ms = 0x118
```
