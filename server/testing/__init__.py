import os
import unittest
import json

from v1.apps import app, db, socketio
from v1.apps.users.models import User

from v1.apps.config import DATABASE_TEST

from flask_socketio import SocketIO, SocketIOTestClient

class TestingBase(unittest.TestCase):
    def initDB(self):
        for i in range(15):
            user = User(username="TestUser" + str(i))
            user.hash_password("password")
            if i == 0:
                user.admin = True
            self.db.session.add(user)
        self.db.session.commit()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_TEST
        self.app = app.test_client()
        self.db = db
        self.db.create_all()
        self.socketio = SocketIOTestClient(app, socketio)
        self.initDB()


    def tearDown(self):
        pass
        self.socketio.disconnect()
        self.db.session.rollback()
        self.db.session.expunge_all()
        self.db.session.flush()
        self.db.session.remove()
        self.db.session.close()
        self.db.drop_all()
