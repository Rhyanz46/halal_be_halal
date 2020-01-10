import json

import pytest
from flask_jwt_extended import get_jwt_identity


class State:
    def __init__(self):
        self.data = {}


@pytest.fixture(scope='session')
def state() -> State:
    state = State()
    state.data['from_fixture'] = 0
    return state


@pytest.mark.parametrize(('username', 'password', 'code'), (
    ('', '', 403),
    ('a', '', 403),
    ('admin', 'admin', 200),
))
def test_login_validate_input(auth, username, password, code) -> None:
    response = auth.login(username, password)
    assert code == response.status_code


def test_login(client, auth, state: State) -> None:
    assert client.get('/user/auth').status_code == 400
    response = auth.login()
    if response.status_code == 200:
        data = json.loads(response.get_data(as_text=True))
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + data['token']
        }
        state.data['header'] = headers
    assert response.status_code == 200


def test_get_my_user(client, state: State) -> None:
    response = client.get('/user', headers=state.data['header'])
    assert response.status_code == 200
    res_data = json.loads(response.data)
    for key in res_data:
        if key == 'email':
            assert type(res_data[key]) == str
        if key == 'id':
            assert type(res_data[key]) == int
        if key == 'user_detail':
            assert type(res_data[key]) == dict
        if key == 'username':
            assert type(res_data[key]) == str
