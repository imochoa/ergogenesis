# Battery sensing and the Pro Micro pin 21 conflict

## Summary

Battery voltage sensing is intentionally disabled on Ergogenesis. The SuperMini
nRF52840's battery voltage divider uses `AIN7`, which is the nRF52840 pin
`P0.31`. ZMK's `nice_nano` board definition also maps Pro Micro pin 21 to
`P0.31`, and Ergogenesis uses pin 21 as a direct key input on both halves.

Enabling a `zmk,battery-voltage-divider` sensor on ADC channel 7 therefore stops
these keys from scanning:

- left half: `middle_home` (`D` on the base layer)
- right half: `inner_top` (`Y` on the base layer)

Battery sensing can only be enabled safely after rerouting those keys or using a
battery-sense circuit connected to a different ADC-capable pin.

## Power and pin terminology

### VDD and VDDH

`VDD` is the normal low-voltage supply for the nRF52840's logic, usually around
3.3 V. `VDDH` is the chip's high-voltage supply input. It accepts approximately
2.5-5.5 V, allowing a LiPo battery, which reaches about 4.2 V when fully
charged, to power it directly. The names come from traditional MOS circuit
notation; the `H` denotes the high-voltage supply.

A genuine nice!nano v2 uses the nRF52840's high-voltage mode approximately as
follows:

```text
LiPo battery
    |
    v
  VDDH ---- internal VDDH/5 measurement ---> ADC
    |
 internal regulator
    |
    v
   VDD ----> nRF52840 logic and low-voltage rail
```

The nRF52840 can measure an internally divided version of VDDH without using an
external GPIO. ZMK therefore describes the nice!nano v2 sensor as:

```dts
compatible = "zmk,battery-nrf-vddh";
```

This measurement method does not conflict with Pro Micro pin 21.

The SuperMini design assumed by this project uses a different power and sensing
arrangement:

```text
LiPo ---> RAW ---> board regulator ---> VDD / 3.3 V
  |
  `---- resistor divider ---> P0.31 / AIN7
```

Measuring VDD would not provide a useful battery level because the regulator
holds it near 3.3 V for most of the discharge cycle. The SuperMini instead
exposes a divided version of the original battery voltage to an ADC-capable
GPIO. SuperMini clones vary, so this circuit and its resistor values must be
confirmed against the actual controller rather than inferred from the
nice!nano-compatible footprint.

### P0.31, D21, A3, and AIN7

The nRF52840 groups its GPIOs into numbered ports:

- port 0 contains `P0.00` through `P0.31`;
- port 1 contains `P1.00` through `P1.15`.

`P0.31` therefore means pin 31 within GPIO port 0. It is not package pin 31 or
Pro Micro pin 31. Devicetree normally represents it as `&gpio0 31`.

A physical SoC pin can have several functions and several names at different
abstraction levels. For this pin, the complete mapping is:

```text
Pro Micro D21 / A3 ---> nRF52840 P0.31 ---> digital GPIO
                                         `-> SAADC input AIN7
```

| Name | Meaning |
|---|---|
| `D21` or Pro Micro pin 21 | Logical connector/header pin |
| `A3` | Pro Micro analog-style connector label |
| `P0.31` | nRF52840 GPIO port 0, pin 31 |
| `AIN7` | nRF52840 SAADC function on `P0.31` |
| `&gpio0 31` | Devicetree representation of `P0.31` |
| `&adc 7` | Devicetree selection of `AIN7` |

The ZMK board mapping makes the connector-to-SoC relationship explicit:

```dts
<21 0 &gpio0 31 0> /* D21/A3 */
```

Consequently, these two declarations request different functions of the same
physical pin:

```dts
input-gpios = <&pro_micro 21 (GPIO_ACTIVE_LOW | GPIO_PULL_UP)>;
io-channels = <&adc 7>;
```

The first uses `P0.31` as a digital key input; the second uses it as analog input
`AIN7` for battery measurement.

## History

The relevant commits are:

```text
8a66947  trying to measure battery level
a6fb741  fixed battery conflicts
```

Commit `8a66947` added a battery node similar to:

```dts
/ {
    chosen {
        zmk,battery = &vbatt;
    };

    vbatt: vbatt {
        compatible = "zmk,battery-voltage-divider";
        io-channels = <&adc 7>;
        output-ohms = <1000000>;
        full-ohms = <2000000>;
    };
};
```

This made battery measurement available, but ADC channel 7 took over the same
physical pin used by the key scanner. Commit `a6fb741` removed the sensor and
split battery forwarding after the `D` and `Y` failures were identified.

Before that change, the build targeted the base `nice_nano` board without a
revision overlay that supplied a suitable `zmk,battery` node. ZMK could still
expose battery reporting while having no real battery sensor, resulting in a
level that remained around its default value. A visible battery service or
`CONFIG_ZMK_BATTERY_REPORTING=y` does not by itself prove that voltage is being
measured.

## Where the conflict is recorded

The repository contains warnings at the points most likely to be edited:

- `README.md` — user-facing explanation
- `config/ergogenesis.conf` — battery sensing and split forwarding are disabled
- `config/boards/shields/ergogenesis/ergogenesis.dtsi` — warning beside the
  left-half pin 21 key input
- `config/boards/shields/ergogenesis/ergogenesis_right.overlay` — warning beside
  the right-half pin 21 key input

The underlying board mapping is in the west-managed ZMK source:

```text
zmk/app/module/boards/nicekeyboards/nice_nano/arduino_pro_micro_pins.dtsi
```

It contains:

```dts
<21 0 &gpio0 31 0> /* D21/A3 */
```

The full resource chain is therefore:

```text
battery voltage divider -> SAADC AIN7 -> nRF52840 P0.31
Pro Micro pin 21        -> GPIO0 pin 31 -> nRF52840 P0.31
kscan key input         -> Pro Micro pin 21
```

`A3` is the connector's analog-style label; `AIN7` is the nRF52840 SAADC input
connected to the same physical SoC pin.

## Why the build did not catch it

Devicetree validation does not generally detect this conflict. The key scanner
references a GPIO through the Pro Micro connector mapping, while the battery
sensor references an ADC channel:

```dts
input-gpios = <&pro_micro 21 (GPIO_ACTIVE_LOW | GPIO_PULL_UP)>;
io-channels = <&adc 7>;
```

Both declarations are valid independently. The relationship between SAADC
channel 7 and `P0.31` is fixed by the nRF52840 hardware and is not represented as
a shared devicetree resource with exclusive ownership. Consequently, `dtc` can
compile both uses without warning even though they conflict at runtime.

The generated devicetree provides the evidence, but identifying the conflict
requires resolving connector aliases and peripheral channels down to physical
SoC pins.

## Resource-audit procedure for future changes

Use this procedure before adding any ADC, SPI, I2C, UART, PWM, LED, display, or
other pin-using feature.

### 1. Identify the actual hardware resource

Consult the controller schematic or trusted pinout and the nRF52840 product
specification. Do not assume that a SuperMini clone has the same battery circuit
as a nice!nano revision merely because it uses the same ZMK board target.

Record:

- the physical SoC GPIO, such as `P0.31`
- alternate peripheral functions, such as `AIN7`
- onboard circuitry already attached to the pin
- whether the function is present on every controller variant in use

### 2. Resolve connector pin aliases

For every `&pro_micro N` reference, inspect the active board's `gpio-map` and
translate it to `gpio0` or `gpio1`. For example:

```text
&pro_micro 21 -> &gpio0 31 -> P0.31
```

Do this for both halves. Ergogenesis is reversible and reverse-mounts the MCU,
so the same controller pin can correspond to different physical keys on the two
halves.

### 3. Compare all consumers

Search the shield, board, and generated configuration:

```bash
rg -n 'input-gpios|io-channels|gpios|pwms|pinctrl|zmk,battery' \
  config/boards zmk/app/module/boards/nicekeyboards/nice_nano
```

Build a small resource table when a change uses more than one pin:

| SoC resource | Connector pin | Existing consumer | Proposed consumer |
|---|---:|---|---|
| `P0.31 / AIN7` | Pro Micro 21 | direct key input | battery ADC |

A physical resource should not have two active consumers unless the hardware and
drivers explicitly support sharing it.

### 4. Inspect the resolved build outputs

Build both halves and generate the reports:

```bash
# From firmware/
just build-all
just devicetree-report-all
just kconfig-report-all

# Or from the repository root
just firmware build-all
just firmware devicetree-report-all
just firmware kconfig-report-all
```

Inspect each target, not only the central half:

```text
.build/nice_nano/ergogenesis_left/zephyr/zephyr.dts
.build/nice_nano/ergogenesis_left/zephyr/.config
.build/nice_nano/ergogenesis_left/zephyr/devicetree-report.html
.build/nice_nano/ergogenesis_left/zephyr/kconfig-report.html

.build/nice_nano/ergogenesis_right/zephyr/zephyr.dts
.build/nice_nano/ergogenesis_right/zephyr/.config
.build/nice_nano/ergogenesis_right/zephyr/devicetree-report.html
.build/nice_nano/ergogenesis_right/zephyr/kconfig-report.html
```

Verify all of the following:

- `chosen.zmk,battery` points to the intended sensor.
- The intended sensor node exists and has `status = "okay"` where applicable.
- `io-channels` uses the expected ADC channel.
- The resolved `gpio-map` agrees with the controller pinout.
- Neither half's `kscan0.input-gpios` resolves to the same physical pin.
- Kconfig enables the actual battery sensor, not only battery reporting or split
  proxying.

The CI recipe also publishes `zephyr.dts`, the combined `.config`, and both HTML
reports under each target's `debug/` artifact directory.

### 5. Perform a hardware smoke test

A successful build is not sufficient for pin multiplexing changes. Before
relying on battery readings:

1. Test every key on both halves.
2. Confirm that battery voltage changes over time rather than remaining at a
   default value.
3. Compare the reported voltage or percentage with a multimeter.
4. Test USB-powered and battery-powered operation.
5. Verify central and peripheral battery reporting separately before enabling
   split fetching or proxying.

## Safe ways to restore battery measurement

Possible hardware solutions are:

1. Reroute both keys currently connected to Pro Micro pin 21 to unused GPIOs.
2. Use a controller whose battery sensor does not consume a key-scanning pin.
3. Add a battery divider on another suitable ADC-capable GPIO and describe its
   actual resistor values in devicetree.

Do not simply re-enable `io-channels = <&adc 7>` or the split battery Kconfig
options. Split fetching and proxying only transport readings; they cannot fix a
missing or conflicting physical sensor.
