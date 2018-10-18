#!/usr/bin/env python3

import argparse
import signal
import sys
import time
import json

from rpi_rf import RFDevice

rfdevice = None
GPIO_PIN = 23


def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, exithandler)

    rfdevice = RFDevice(GPIO_PIN)
    rfdevice.enable_rx()

    timestamp = None
    while True:
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp

            d = dict()
            d["code"] = rfdevice.rx_code
            d["pulselength"] = rfdevice.rx_pulselength
            d["protocol"] = rfdevice.rx_proto
            print(json.dump(d))

        time.sleep(0.01)


if __name__ == '__main__':
    main()
