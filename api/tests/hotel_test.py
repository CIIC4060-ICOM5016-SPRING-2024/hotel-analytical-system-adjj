from api.model.db import Database

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

def test_post_hotel(client):
    # Datos del nuevo empleado
    new_hotel = {
        "chid": 5,
        "hname": "Hotel de Janiel",
        "hcity": "Mayaguez",
    }

    # Enviar petición POST al endpoint /hotel con los datos del empleado
    response = client.post('/hotel', json=new_hotel)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['message'] == "Hotel agregado exitosamente", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM hotel 
                    WHERE chid = %s AND hname = %s AND hcity = %s
                    """
        cur.execute(query, (new_hotel['chid'], new_hotel['hname'], new_hotel['hcity']))
        hotel = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert hotel is not None, "El hotel añadido no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el hotel a eliminar
        query = """
                DELETE FROM hotel
                WHERE chid = %s AND hname = %s AND hcity = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (
            new_hotel['chid'],
            new_hotel['hname'],
            new_hotel['hcity']
        )
        # Ejecutar la consulta DELETE
        cur.execute(query, values)
        # Hacer commit de los cambios
        db.conexion.commit()
    except Exception as e:
        print(f"Error al limpiar la base de datos: {e}")
        db.conexion.rollback()
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        cur.close()
    db.close()