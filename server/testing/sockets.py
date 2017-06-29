from . import TestingBase
from v1.apps.users.models import User

import json

class SocketTests(TestingBase):

    def test_login(self):
        username = "TestUser1"
        password = "password"
        self.socketio.emit('login', {
            "username": username,
            "password": password,
        })
        response = self.socketio.get_received()
        latest_response = response[-1]['args'][0]
        assert username in latest_response['user']['username']
