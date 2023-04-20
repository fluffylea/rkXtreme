import json


def _hex_to_rgb(hexadecimal: str):
    r = int(hexadecimal[1:1 + 2], 16)
    g = int(hexadecimal[3:3 + 2], 16)
    b = int(hexadecimal[5:5 + 2], 16)
    return r, g, b


class Message:
    total_payload_length = 433
    payload = bytearray(total_payload_length)

    def __init__(self):
        with open("config.json") as f:
            self.config_map = json.load(f)

            for key in self.config_map:
                entry = self.config_map[key]

                red, green, blue = _hex_to_rgb(entry['color'])

                self.payload[entry['key_id'] * 3] = red
                self.payload[entry['key_id'] * 3 + 1] = green
                self.payload[entry['key_id'] * 3 + 2] = blue

    def to_payload(self) -> list[bytearray]:
        packets = []
        cursor = 0

        # Every payload is split up into 7 packets, each 65 bytes in length
        # The first packet starts with       0a 07 01 06 00 <payload>
        # The remaining 6 packets start with 0a 07 <packet number> <payload>
        for i in range(1, 8):
            packet = bytearray(65)
            for j in range(len(packet)):
                if j == 0:
                    packet[j] = 0x0a
                elif j == 1:
                    packet[j] = 0x07
                elif j == 2:
                    packet[j] = i
                elif j == 3 and i == 1:
                    packet[j] = 0x06
                elif j == 4 and i == 1:
                    packet[j] = 0x00
                else:
                    packet[j] = self.payload[cursor]
                    cursor += 1
            packets.append(packet)
        return packets

    def __str__(self):
        return '\n'.join(':'.join(format(x, '02x') for x in msg) for msg in self.to_payload())
