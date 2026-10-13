# Diode key-matrix revision

This PCB revision keeps the 36-key split layout but replaces one-GPIO-per-key
scanning with a conventional row/column diode matrix. Each half uses nine GPIOs
for 18 keys and leaves Pro Micro D21 dedicated to the SuperMini battery sensor.

## Matrix per half

The switches form a sparse 5-column by 4-row matrix:

| Signal | Pro Micro pin | Keys |
| --- | ---: | --- |
| `row0` | D4 | top row |
| `row1` | D5 | home row |
| `row2` | D6 | bottom row |
| `row3` | D7 | thumbs |
| `col0` | D18 | pinky column |
| `col1` | D19 | ring column |
| `col2` | D20 | middle column and near thumb |
| `col3` | D14 | index column and home thumb |
| `col4` | D15 | inner column and far thumb |

Every switch connects its column to a per-key net. A reversible SOD-123
footprint then connects that net to its row. Populate it with a
1N4148W-compatible diode with the **anode on the switch side** and the
**cathode (striped end) on the row side**. Current flows
`column -> switch -> diode -> row`, matching ZMK's `col2row` scanner.

The matrix leaves D0-D3, D8-D10, D16, and D21 unused. In particular, D21 maps
to nRF52840 P0.31 / AIN7 and is no longer shared with a key.

## Battery reporting

Each half defines a `zmk,battery-voltage-divider` sensor on AIN7. The left half
fetches and proxies the right half's level over the split connection.

The firmware assumes the common SuperMini 1 MΩ + 1 MΩ divider. SuperMini clones
vary, so verify the fitted controller and calibrate `output-ohms` and
`full-ohms` in `ergogenesis.dtsi` against a multimeter before trusting the
reported percentage.

## Reversible right half

Both halves use the same PCB and matrix nets. The right firmware offsets local
columns 0-4 to split columns 5-9. The shared matrix transform reverses those
columns to preserve the existing mirrored keymap order when the PCB is flipped.
The diode footprint is reversible, but diode polarity still matters on whichever
side is populated.

## Source-of-truth files

- `hardware/ergogen/config.yaml`: row/column nets, diode footprints, and MCU pins
- `firmware/config/boards/shields/ergogenesis/ergogenesis.dtsi`: scanner,
  transform, and battery sensor
- `firmware/config/boards/shields/ergogenesis/ergogenesis_right.overlay`: right
  half column offset
- `firmware/config/boards/shields/ergogenesis/Kconfig.defconfig`: split battery
  forwarding

After changing a net, regenerate the PCB and update the corresponding firmware
GPIO declaration. Build and test both halves; a successful firmware build does
not validate diode orientation or PCB routing.
