import json
import tornado.web

from .message import Message

from database.models import tables


class DBHandler(tornado.web.RequestHandler):

    def initialize(self, api):
        self.db_api = api

    def get(self):
        message_str = self.get_argument("message")

        m = Message()
        m.from_dict(json.loads(message_str))
        method = m.method
        data = m.data

        answer = Message()
        if method == "get":
            item = data["item"]
            if item == 'receiver':
                answer = self.get_available_receivers()
        elif method is "set":
            item = data["receiver"]
            field = data["attribute"]
            if item == 'receiver':
                if field == "attribute":
                    answer = self.set_receiver_alias(data)

        self.write_message(answer.__dict__)

    def post(self):
        message_str = self.get_argument("message")

        m = Message()
        m.from_dict(json.loads(message_str))
        method = m.method
        data = m.data

        if method == 'set':
            item = data["receiver"]
            field = data["attribute"]
            if item == 'receiver':
                if field == "attribute":
                    answer = self.set_receiver_alias(data)

    def get_available_receivers(self):
        self.db_api.open()
        receivers = self.db_api.select_all(tables.RFReceiver)
        self.db_api.close()

        answer = Message()
        answer.success = False
        if len(receivers) > 0:
            answer.success = True
            receiver_list = []
            for r in receivers:
                receiver_list.append(r.as_dict())
            answer.data = receiver_list

        return answer

    def set_receiver_alias(self, data):
        answer = Message()

        self.db_api.open()
        receiver = self.db_api.select(tables.RFReceiver, tables.RFReceiver.id == data['receiver'])
        if receiver is not None:
            receiver.alias = data['alias']
            self.db_api.commit()
            self.db_api.close()
            answer.success = True
        else:
            self.db_api.close()
            answer.data = {'error': "The selected Receiver seems not to be in the database!"}
            return answer

        self.db_api.close()

        return answer
