import database.base
from .models import tables
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

class Api(object):
    def __init__(self, bind):
        self._db = None
        self.bind = bind

    def open(self):
        ''' creates a session for database transaction if none is active. '''
        if not self.is_open():
            self._db = Session(bind=self.bind)

    def close(self):
        ''' closes the current database session if open. '''
        if self.is_open():
            self._db.expunge_all()
            self._db.close()
            self._db = None

    def _clear(self):
        ''' clears all tables '''
        # self.ensure_open()

        for table in reversed(database.base.TableBase.metadata.sorted_tables):
            self._db.execute(table.delete())

        return self.commit()

    def commit(self):
        ''' Commits changed content left in session.
            Automatic rollback is performed if errror occurs.
            Returns success of transaction. '''
        if self.is_open():
            try:
                self._db.commit()
                return True
            except exc.SQLAlchemyError as e:
                print("FAILURE:", e)
                self._db.rollback()
                return False
        else:
            print("Notification: Session not open, nothing to commit.")
            return False

    def is_open(self):
        ''' Returns true if the current session is active, false otherwise. '''
        return self._db != None

    def ensure_open(self):
        ''' checks if database session is open and opens if not. '''
        if not self.is_open():
            self.open()

    def insert(self, obj):
        ''' adds a database object to the current session. '''
        if self.is_open():
            self._db.add(obj)
        else:
            print("Notification: Session not open, nothing to add.")

    def insert_all(self, obj_list):
        ''' adds a list of database objects to the current session. '''
        if self.is_open():
            self._db.add_all(obj_list)
        else:
            print("Notification: Session not open, nothing to add.")

    def expunge(self, obj):
        ''' removes a database object from the current session. '''
        if self.is_open():
            self._db.expunge(obj)
        else:
            print("Notification: Session not open, nothing to remove.")

    def expunge_all(self, obj_list):
        ''' removes a list of database objects from the current session. '''
        if self.is_open():
            for item in obj_list:
                self._db.expunge(item)
        else:
            print("Notification: Session not open, nothing to remove.")

    def delete(self, obj):
        ''' Helper function to encapsulate delete operations.
            Performs automatic commit (see commit()).
            Performs automatic expunge if commit unsuccessful (see expunge()).
            Returns success of operation. '''
        # self.ensure_open()
        self._db.delete(obj)
        if not self.commit():
            self._db.expunge(obj)
            return False
        return True

    def query(self, *args):
        ''' universal function for querying the database connection. '''
        # self.ensure_open()
        return self._db.query(*args)

    def select(self, table, filter):
        ''' helper function for performing simple select operations. '''
        return self.query(table).filter(filter)

    def select_all(self, table):
        ''' helper function for performing select operations with no filter. '''
        # return self.query(table).filter(filter)
        return self.query(table).all()
