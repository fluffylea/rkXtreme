# rkXtreme

Individually addressable LEDs on RK-Keyboards.

The default config.json provided has the keymap for the RK100.
The keymap can be found in the install-directory of the [RK Keyboard Software](https://bit.ly/RKRGBSOFT).

## Requirements

* Windows
* Python 3
* RK Keyboard

## Technical Information

The Keyboard uses HID feature reports to set and update the LEDs. 
It encodes its payload into 7 packets, with each packet being a size of 65 bytes.

They are structured like following:

* First packet: `0a 07 01 06 00 <payload>`
* Further packets: `0a 07 <packet number> <payload>`

The payload itself contains a 3-byte RGB value for each key on the keyboard.
The offset of the keys can be found in the KB.ini file from the official software, 
where it is the last column in the `[KEY]` section.

When the keyboard does not receive such a packet for a while, it switches back to the 
color mode it was on before.