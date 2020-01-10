import os
import tempfile

import pytest
import json
from app import create_app


@pytest.fixture(scope="module")
def app():
    db_fd, db_path = tempfile.mkstemp()
    # from sys import breakpointhook
    # breakpointhook()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        yield app

    print("akhir")
    os.close(db_fd)
    os.unlink(db_path)


class AuthActions(object):
    def __init__(self, client):
        self._client = client
        self.headers = None

    def login(self, username='admin', password='admin'):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = self._client.post(
            '/user/auth', data=json.dumps({'username': username, 'password': password}), headers=headers
        )
        return response

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def client(app):
    client_ = app.test_client()
    return client_


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
