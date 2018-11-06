from rpi_rf import RFDevice

class RFSender(object):
    def __init__(self, pin):
        self.pin = pin
        self.device = RFDevice(pin)
        self.device.enable_tx()

    def __del__(self):
        self.device.cleanup()

    def transmit(self, signal):
        # print("Transmitting code: ", signal.code, signal.protocol, signal.pulselength)
        self.device.tx_code(signal.code, signal.protocol, signal.pulselength)
