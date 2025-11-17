https://github.com/zmkfirmware/zmk/blob/main/app/boards/shields/cradio/README.md


# [https://zmk.dev/docs/development/hardware-integration/new-shield?keyboard-type=split#kscan](Kscan)

> **ZMK uses the blue color coded "Arduino" pin names to generate devicetree node references.**
For example, to refer to the pin labeled 0 in the diagram, use &pro_micro 0 in the devicetree files.


# Mapping pin numbers...
https://github.com/zmkfirmware/zmk/blob/4ec69cb7e658590adf6354027aca789b364a70c5/app/boards/arm/nrfmicro/arduino_pro_micro_pins.dtsi

`.dtsi` names are NOT the pin numbers!

https://github.com/zmkfirmware/zmk/blob/main/app/boards/shields/cradio/cradio.dtsi


https://github.com/zmkfirmware/zmk/tree/4ec69cb7e658590adf6354027aca789b364a70c5/app/boards/arm/nice_nano

https://github.com/zmkfirmware/zmk/blob/4ec69cb7e658590adf6354027aca789b364a70c5/app/boards/arm/nice_nano/arduino_pro_micro_pins.dtsi



PIN#? | ???? | D
-- | -- | --
0  | 8  | D0
1  | 6  | D1
2  | 17 | D2
3  | 20 | D3
4  | 22 | D4/A6
5  | 24 | D5
6  | 0  | D6/A7
7  | 11 | D7
8  | 4  | D8/A8
9  | 6  | D9/A9
10 | 9  | D10/A10
16 | 10 | D16
14 | 11 | D14
15 | 13 | D15
18 | 15 | D18/A0
19 | 2  | D19/A1
20 | 29 | D20/A2
21 | 31 | D21/A3

## Changing the pin numbers
https://github.com/zmkfirmware/zmk/tree/main/app/boards/shields/cradio#pin-arrangement
