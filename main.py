import time
from pprint import pprint

import pywinusb.hid as hid
from pywinusb.hid.core import HidDevice

from message import Message


def main(target_vendor_id, target_report_id):
    # Generate messages from config
    message = Message()
    print(message)
    payload = message.to_payload()

    # get devices
    all_devices: list[HidDevice] = hid.HidDeviceFilter(vendor_id=target_vendor_id).get_devices()
    pprint(all_devices)

    for device in all_devices:
        try:
            device.open()
            reports = device.find_any_reports()
            for value in reports.values():
                for report in value:
                    if report.report_id != target_report_id:
                        continue
                    while True:
                        # If we don't send the payload often enough, the keyboard
                        # will return to its previous state
                        for packet in payload:
                            report.send(packet)
                        time.sleep(0.5)
        finally:
            device.close()


if __name__ == '__main__':
    main(target_vendor_id=0x258a, target_report_id=0x0a)
