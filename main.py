import sys, json

import tornado.ioloop
import tornado.web
import tornado.websocket

import database.base
from database.api import Api
from database.models import tables

from lib.interaction_handler import InteractionHandler
from lib.db_handler import DBHandler
from lib.rf_sender import RFSender

PORT = 8888


def load_json_file(filename):
    str_data = ""
    with open(filename, 'r') as file:
        str_data = file.read()
    return json.loads(str_data)


def set_database_to_default(recreate=True):
    """
    reset database
    :param recreate:
    :return:
    """
    a = None
    if recreate:
        database.base.recreate_database()
        a = Api(bind=database.base.engine)
    else:
        a = Api(bind=database.base.engine)
        a._clear()
    a.close()
    del a
    a = None


def create_swtichable_db_entries(api):
    # load config and create plug list
    config = load_json_file("keys.json")
    for element in config['receiver']:
        api.open()

        # create signals
        on_signal = tables.RFSignal()
        on_signal.code = element["signal"]['on']['code']
        on_signal.pulselength = element["signal"]['on']['pulselength']
        on_signal.protocol = element["signal"]['on']['protocol']

        off_signal = tables.RFSignal()
        off_signal.code = element["signal"]['off']['code']
        off_signal.pulselength = element["signal"]['off']['pulselength']
        off_signal.protocol = element["signal"]['off']['protocol']

        api.insert(on_signal)
        api.insert(off_signal)
        api.commit()

        # create receiver
        receiver = tables.RFReceiver()
        receiver.name = element['name']
        receiver.on_signal_id = on_signal.id
        receiver.off_signal_id = off_signal.id

        api.insert(receiver)
        api.commit()
        api.close()


def db_test(api):
    # some tests
    api.open()
    foo = api.select_all(tables.RFReceiver)
    api.close()
    for e in foo:
        print(e.state)


def main():
    # establish database connection interface
    api = Api(bind=database.base.engine)
    # perform_db_tests(api)

    set_database_to_default(True)
    create_swtichable_db_entries(api)
    db_test(api)

    ### create sender module
    sender = RFSender(17)

    # define handlers
    app = tornado.web.Application([
        (r"/interaction", InteractionHandler, dict(api=api, sender=sender)),
        (r"/db", DBHandler, dict(api=api))
    ])
    app.listen(PORT)

    # print("Starting tornado server on port %i" % PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
