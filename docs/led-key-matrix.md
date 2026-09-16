# LED and key-matrix revision

This revision keeps the 36-key physical layout and reversible split PCB, but
replaces direct GPIO scanning with a diode matrix and adds per-key RGB.

## Electrical layout per half

The 18 switches use a 5-column by 4-row, column-to-row matrix:

| Signal | Pro Micro pin | Keys |
| --- | --- | --- |
| `row0` | D4 | top row |
| `row1` | D5 | home row |
| `row2` | D6 | bottom row |
| `row3` | D7 | thumbs |
| `col0` | D18 | pinky column |
| `col1` | D19 | ring column |
| `col2` | D20 | middle column and near thumb |
| `col3` | D14 | index column and home thumb |
| `col4` | D15 | inner column and far thumb |
| `LED_DATA` | D16 / nRF P0.10 | first SK6812 DIN |

Each switch connects its column to a per-key net. A 1N4148W-compatible SOD-123
diode connects that net to its row, with current flowing from column to row.
This matches ZMK's `diode-direction = "col2row"` setting.

The matrix uses 9 GPIOs instead of 18. RGB uses one more, leaving D0-D3,
D8-D10, and D21 available. D21 is intentionally free so battery sensing does
not conflict with key scanning.

## RGB chain

Each key has a reversible, reverse-mounted SK6812 MINI-E footprint aligned with
the Choc v1 LED window. Populate LEDs on the side opposite the switches. The
footprints include their required PCB cutouts and connect to `VCC` and `GND`.

The data path starts at `inner_top`, snakes through the three alpha rows and
thumb cluster, and ends at `pinky_bottom` on `LED_OUT`. The exact sequence is
encoded by each point's `led_in` and `led_out` properties in
`hardware/ergogen/config.yaml`.

ZMK drives 18 LEDs on each half through SPI3. Firmware limits brightness to 20%
and starts at 10% to reduce battery load. RGB controls are on the first row of
the Control layer.

## Reversible right half

Both halves use the same PCB and matrix nets. The right firmware applies a
five-column split offset, while the shared transform reverses right-hand
columns to preserve the existing 36-key keymap order. The reversible diode and
LED footprints preserve net polarity when components are populated on the
opposite side.

## Source-of-truth files

- `hardware/ergogen/config.yaml`: matrix nets, diodes, LED chain, and MCU pins
- `firmware/config/boards/shields/ergogenesis/ergogenesis.dtsi`: scanner,
  transform, and SPI LED strip
- `firmware/config/boards/shields/ergogenesis/ergogenesis_right.overlay`: right
  half column offset
- `firmware/config/ergogenesis.conf`: RGB settings

After changing any matrix net, regenerate the PCB and update the corresponding
ZMK GPIO declaration before building both firmware halves.
