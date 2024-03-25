import pytest
from api.app import create_app

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    response = client.get('/')
    assert response.data == b'Hello World!'
    assert response.status_code == 200

def test_get_all_clients(client):
    response = client.get('/client')
    assert response.status_code == 200, "response code should be 200 but got {}".format(response.status_code)
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'age' in data[i], "age has to be a key"
            assert 'clid' in data[i], "clid has to be a key"
            assert 'fname' in data[i], "fname has to be a key"
            assert 'lname' in data[i], "lname has to be a key"
            assert 'memberyear' in data[i], "memberyear has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['age'], int)
            assert isinstance(data[i]['clid'], int)
            assert isinstance(data[i]['fname'], str)
            assert isinstance(data[i]['lname'], str)
            assert isinstance(data[i]['memberyear'], int)

