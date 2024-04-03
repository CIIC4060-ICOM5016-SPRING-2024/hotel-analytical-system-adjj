from api.model.db import Database

def test_hello_world(client):
    response = client.get('/')
    assert response.data == b'Hello World!'
    assert response.status_code == 200

