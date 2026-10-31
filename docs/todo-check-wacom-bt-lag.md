# Check Wacom Bluetooth lag with Ergogenesis

Started: 2026-09-16

## Symptom

Wacom mouse movement becomes laggy when Ergogenesis is connected over Bluetooth. The keyboard itself remains responsive, with no observed delayed or dropped keystrokes.

This does not yet identify the faulty device. Pointer input is continuous and makes delayed Bluetooth packets much easier to notice than keyboard input. The keyboard also has a stronger-than-default transmit-power setting.

Still to establish:

- [ ] Does the lag occur while the keyboard is idle, or only while typing?
- [ ] Does it start immediately after Ergogenesis connects?
- [ ] Does disconnecting Ergogenesis immediately stop the lag?
- [ ] Does the Wacom lag with other Bluetooth keyboards?
- [ ] Do other Bluetooth pointing devices lag alongside Ergogenesis?

## Relevant ZMK configuration

The current settings are in `firmware/config/ergogenesis.conf`:

```ini
CONFIG_ZMK_BLE=y
CONFIG_ZMK_BLE_EXPERIMENTAL_CONN=y
CONFIG_BT_CTLR_TX_PWR_PLUS_8=y
CONFIG_ZMK_SPLIT_BLE=y
```

Points to check:

- `CONFIG_BT_CTLR_TX_PWR_PLUS_8=y` sets the nRF52840 radio to +8 dBm. This gives the keyboard a strong link but may make close-range RF interference worse. It does not by itself increase airtime.
- In the current ZMK version, `CONFIG_ZMK_BLE_EXPERIMENTAL_CONN=y` disables 2M PHY. Falling back to 1M PHY can require more airtime, although HID packets are small.
- Ergogenesis is split over BLE. The left half communicates with the host and the right half, so there is another radio link beyond the Wacom-to-host connection.
- The generated firmware requests a 7.5-15 ms host connection interval with peripheral latency 30. Do not tune this until the simpler tests below are complete.

## Working hypothesis

The first hypothesis is an RF-coexistence or host Bluetooth scheduling problem rather than a general Ergogenesis connection failure. A Wacom pointer sends frequent, latency-sensitive reports, while sparse keyboard reports can appear normal under the same conditions.

The main alternatives are a weak Wacom link, a Wacom driver or firmware issue, macOS Bluetooth scheduling, or unrelated 2.4 GHz interference.

## Test plan

Change one variable at a time and record the result.

1. Establish a baseline with the Wacom connected and both keyboard halves powered off.
2. Connect Ergogenesis and compare the Wacom while the keyboard is idle and while typing continuously.
3. Disconnect Ergogenesis from the host. If necessary, power off both halves as a separate test so that neither split traffic nor advertising remains.
4. Increase the distance between the Wacom and the left keyboard half. The left half is the split central.
5. Temporarily move nearby Wi-Fi traffic to 5 or 6 GHz and move USB 3 devices or hubs away from the host and tablet.
6. Build firmware without `CONFIG_BT_CTLR_TX_PWR_PLUS_8=y`, using a pristine build, then repeat the baseline.
7. If the lag remains, restore the previous test state and build without `CONFIG_ZMK_BLE_EXPERIMENTAL_CONN=y`. Repeat the baseline.
8. Only after those tests, investigate connection intervals, Wacom firmware/driver updates, and re-pairing.

## Results

| Date | Keyboard state/configuration | Wacom behavior | Keyboard behavior | Notes |
| --- | --- | --- | --- | --- |
| 2026-09-16 | Current configuration | Mouse movement lags | No observed lag or dropped keys | Initial report |

## Firmware test notes

A change to `ergogenesis.conf` requires a pristine rebuild:

```sh
just firmware build-firmware
```

Keep each test firmware long enough to compare the same tablet position, host workload, and Wi-Fi conditions. Restore settings between tests if needed so that each result changes only one variable.
