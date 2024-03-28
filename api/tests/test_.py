import pytest
from api.wsgi import create_app

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
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
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



def test_get_all_employees(client):
    response = client.get('/employee')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'age' in data[i], "age has to be a key"
            assert 'eid' in data[i], "eid has to be a key"
            assert 'fname' in data[i], "fname has to be a key"
            assert 'lname' in data[i], "lname has to be a key"
            assert 'position' in data[i], "position has to be a key"
            assert 'salary' in data[i], "salary has to be a key"
            assert 'hid' in data[i], "hid has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['age'], int), "age has to be integer"
            assert isinstance(data[i]['eid'], int), "eid has to be integer"
            assert isinstance(data[i]['fname'], str), "fname has to be string"
            assert isinstance(data[i]['lname'], str), "lname has to be string"
            assert ((isinstance(data[i]['position'], str) and
                    data[i]['position'] == 'Regular' or
                    data[i]['position'] == 'Supervisor') or
                    data[i]['position'] == 'Administrator'), "position has to be string and must be Regular, Supervisor or Administrator"

            assert isinstance(data[i]['salary'], float), f"salary has to be float but got {type(data[i]['salary'])}"
            assert data[i]['position'] == 'Regular' and 18000 <= data[i]['salary'] <= 49999 or \
            data[i]['position'] == 'Supervisor' and 50000 <= data[i]['salary'] <= 79999 or \
            data[i]['position'] == 'Administrator' and 80000 <= data[i]['salary'] <= 120000, \
                (f"Position=Regular 18000 <= Salary <= 49999"
                 f"Position=Supervisor 50000 <= Salary <= 79000"
                 f"Position=Administrator 80000 <= Salary <= 120000"
                 f"But got {data[i]['salary']}")

            assert isinstance(data[i]['hid'], int), f"hid has to be int but got {type(data[i]['hid'])}"


