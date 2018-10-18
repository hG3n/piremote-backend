import json
import tornado.websocket
from .message import Message

from database.models import tables


class InteractionHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, api, sender):
        self.db_api = api
        self.rf_sender = sender

    def check_origin(self, origin):
        print("origin: ".format(origin))
        return True

    def open(self):
        print("InteractionHandler: A client connected.")

    def on_close(self):
        print("InteractionHandler: A client disconnected")

    def on_message(self, message):
        print("received message:", message)

        m = Message()
        m.from_dict(json.loads(message))
        method = m.method
        data = m.data

        answer = Message()
        if method == "toggle":
            answer = self.toggle_receiver(data)

        print(answer)
        self.write_message(answer.__dict__)

    def toggle_receiver(self, data):
        receiver_id = data["receiver"]
        signal_id = data["signal"]
        state = data["state"]

        # check fo signal
        self.db_api.open()
        signal_obj = self.db_api.select(tables.RFSignal, tables.RFSignal.id == signal_id).first()
        self.db_api.close()

        answer = Message()
        answer.method = "reload"
        if signal_obj is not None:
            self.db_api.open()
            receiver_obj = self.db_api.select(tables.RFReceiver, tables.RFReceiver.id == receiver_id).first()

            if receiver_obj is not None:
                self.rf_sender.transmit(signal_obj)
                receiver_obj.state = state
                self.db_api.commit()
                answer.success = True
            else:
                answer.success = False

        self.db_api.close()
        return answer
