# PCB revision issues

## Battery reporting conflicts with the P21 key input

Status: resolved by the diode-matrix PCB revision

The direct-pin revision had working battery-reporting plumbing, but its ADC pin
was also configured as a key input. The diode-matrix revision reduces each
half's scanner from 18 GPIOs to nine and leaves D21 / AIN7 dedicated to battery
measurement. The details below remain as historical context for direct-pin
PCBs.

The SuperMini's battery divider is connected to nRF52840 `P0.31` / `AIN7`.
That is also Pro Micro `D21` (`P21`), which this PCB uses as a direct key input:

- left half: `middle_home`
- right half: `inner_top`

Both mappings configure the pin as an active-low input with `GPIO_PULL_UP`. The
nRF52840's internal pull-up is much stronger than the assumed 1 MΩ + 1 MΩ
SuperMini divider, so it pulls the ADC input close to 3.3 V. Firmware then
applies the divider's 2:1 scale, obtains an apparent voltage above 4.2 V, and
clamps the reported charge to 100%.

Relevant files:

- `hardware/ergogen/config.yaml`, `pcbs.shield-pcb.footprints.mcu-fp.P21`
- `firmware/config/boards/shields/ergogenesis/ergogenesis.dtsi`
- `firmware/config/boards/shields/ergogenesis/ergogenesis_right.overlay`

### Implemented fix

The PCB now uses a 5x4 diode matrix per half. Nine row/column GPIOs replace the
18 direct key inputs, and `P21` is no longer connected to the scanner. `P0.31`
is dedicated to ZMK's standard battery-voltage-divider driver. See
[`diode-key-matrix.md`](diode-key-matrix.md) for the net and pin map.

### Keeping P21 connected to a key

It is possible to share the pin, but the battery network must also act as the
key's pull-up. Do not enable the nRF52840 internal pull-up.

Design the effective divider so that its midpoint:

1. stays above the GPIO input-high threshold at the lowest usable battery
   voltage; and
2. stays below the ADC input limit at the highest charging voltage.

For a 3.3 V GPIO supply, a 3.45-4.20 V LiPo range, and the SAADC configuration
currently used by ZMK, a midpoint near 75% of battery voltage is a reasonable
starting target. It gives approximately 2.59-3.15 V. Those figures need to be
checked against the nRF52840 electrical specification and real controller
boards before choosing parts.

If the SuperMini really has a 1 MΩ upper and 1 MΩ lower resistor, adding roughly
499 kΩ from switched battery power (`RAW`) to `P0.31` puts that resistor in
parallel with the upper 1 MΩ resistor and moves the ratio close to 75%. This is
only an example calculation. SuperMini clones do not necessarily use the same
resistor values, so measure the fitted board or obtain its schematic first.
The devicetree `output-ohms` and `full-ohms` values must match the resulting
network.

Sharing still needs firmware work:

- configure the P21 key input without `GPIO_PULL_UP`;
- reject or retry a battery sample while the key is held, since pressing it
  grounds the ADC input and otherwise looks like an empty battery;
- preserve the previous battery value when a sample is rejected; and
- verify that suspend/resume does not re-enable an internal pull.

A custom battery sensor driver may be needed for the sample filtering. The
stock voltage-divider driver will accept a grounded sample and report 0%.

An analog switch could instead alternate `P0.31` between the key and battery
divider, but it adds parts, requires another control signal, and still needs
sampling coordination in firmware. Moving the key to an extra MCU pin is
simpler and less fragile.

### Verification for the next revision

- Measure battery voltage and `P0.31` voltage with USB disconnected at full,
  mid, and near-empty charge.
- Check the calculated voltage against a multimeter before trusting the
  percentage.
- Test the P21 key across the full battery range.
- Hold and repeatedly press the P21 key across several 60-second battery sample
  intervals; the reported level must not jump to 0% or 100%.
- Verify both local and peripheral battery values on the central half.
- Repeat while charging over USB and after suspend/resume.
