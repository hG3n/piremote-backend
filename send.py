#!/usr/bin/env python3
import argparse
import json
from rpi_rf import RFDevice

GPIO_PIN = 17

class RFSignal(object):

    def __init__(self):
        self.name = None
        self.code = None
        self.pulselength = None
        self.protocol = None

    def from_json(self, json_data):
        self.code = json_data["code"]
        self.pulselength = json_data["pulselength"]
        self.protocol = json_data["protocol"]


class RFReceiver(object):
    def __init__(self):
        self.name = None
        self.on_signal = RFSignal()
        self.off_signal = RFSignal()

    def from_json(self, json_data):
        self.name = json_data['name']
        self.on_signal = RFSignal()
        self.on_signal.from_json(json_data['signal']['on'])
        self.off_signal.from_json(json_data['signal']['off'])


class RFSender(object):
    def __init__(self, pin):
        self.pin = pin
        self.device = RFDevice(pin)
        self.device.enable_tx()

    def __del__(self):
        self.device.cleanup()

    def transmit(self, signal):
        self.device.tx_code(signal.code, signal.protocol, signal.pulselength)


def load_json_file(filename):
    str_data = ""
    with open(filename, 'r') as file:
        str_data = file.read()
    return json.loads(str_data)


def main():
    # create cmd line parser
    parser = argparse.ArgumentParser(description='Sends a decimal code via a 433/315MHz GPIO device')
    parser.add_argument('-p', dest='plug', type=str, default=None, help="Plug to toggle")
    parser.add_argument('-s', dest='state', type=int, default=None, help="Specify state (0 || 1)")
    args = parser.parse_args()

    # just exit if there are no arguments
    if args.plug is None or args.state is None:
        print("Error: no option selected!")
        print("exiting...")
        return

    # load config and create plug list
    config = load_json_file("keys.json")
    receiver_list = []
    for element in config['keys']:
        r = RFReceiver()
        r.from_json(element)
        receiver_list.append(r)

    # create sender module
    sender = RFSender(GPIO_PIN)

    # execute the given command
    for r in receiver_list:
        if r.name == args.plug:
            if args.state == 0:
                sender.transmit(r.off_signal)
            else:
                sender.transmit(r.on_signal)


if __name__ == "__main__":
    main()
