

def test_get_all_hotels(client):
    response = client.get('/hotel')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'hid' in data[i], "hid has to be a key"
            assert 'chid' in data[i], "chid has to be a key"
            assert 'hname' in data[i], "hname has to be a key"
            assert 'hcity' in data[i], "hcity has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['hid'], int), f"hid has to be int but got {type(data[i]['hid'])}"
            assert isinstance(data[i]['chid'], int), f"eid has to be integer but got {type(data[i]['chid'])}"
            assert isinstance(data[i]['hname'], str), f"fname has to be string but got {type(data[i]['hname'])}"
            assert isinstance(data[i]['hcity'], str), f"lname has to be string but got {type(data[i]['hcity'])}"
