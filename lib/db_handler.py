import json
import tornado.web

from .message import Message

from database.models import tables


class DBHandler(tornado.web.RequestHandler):

    def initialize(self, api):
        self.db_api = api

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        fct = self.get_argument("fct")

        answer = Message()
        if fct == "get_available_switchables":
            answer = self.get_available_receivers()

        print('sending message')
        self.write(answer.__dict__)

    def post(self):
        db_request = json.loads(self.request.body.decode("utf-8"))
        fct = db_request['function']

        answer = Message()
        if fct == 'set_receiver_alias':
            answer = self.set_receiver_alias(db_request)

        self.write(answer.__dict__)

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

        element_id = data['element_id']
        field = data['field']
        value = data['value']

        self.db_api.open()
        receiver = self.db_api.select(tables.RFReceiver, tables.RFReceiver.id == element_id).first()
        if receiver is not None:
            if field == 'alias':
                receiver.alias = value



            self.db_api.commit()
            self.db_api.close()
            answer.success = True
        else:
            self.db_api.close()
            answer.data = {'error': "The selected Receiver seems not to be in the database!"}
            return answer

        self.db_api.close()

        return answer
