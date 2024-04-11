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

def test_get_hotel_by_id(client):
    # Asumiendo que ya tienes un hotel en tu base de datos de prueba, utiliza ese ID. De lo contrario, inserta uno y obtén el ID.
    # Reemplaza esto con un ID válido de tu base de datos de prueba o después de insertar un hotel nuevo
    for hid in range(1,41):
        response = client.get(f'/hotel/{hid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"

        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'hid' in data, "'hid' debe estar presente"
        assert 'chid' in data, "'chid' debe estar presente"
        assert 'hname' in data, "'hname' debe estar presente"
        assert 'hcity' in data, "'hcity' debe estar presente"
        assert isinstance(data['hid'], int), "hid debe ser un entero"
        assert isinstance(data['chid'], int), "chid debe ser un entero"
        assert isinstance(data['hname'], str), "hname debe ser una cadena"
        assert isinstance(data['hcity'], str), "hcity debe ser una cadena"

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
    assert response_data['status'] == "success", "Expected success message in the response"

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





def test_delete_hotel(client):
    # Paso 1: Añadir un nuevo empleado directamente a la base de datos y obtener su eid
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO hotel (chid, hname, hcity) 
            VALUES (%s, %s, %s) RETURNING hid""",
                    (5, "Hotel de Janiel", "Mayaguez"))
        hid = cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el hid del nuevo registro
        db.conexion.commit()
    except Exception as e:
        print(f"Error al añadir hotel para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir hotel para prueba de eliminación"
    finally:
        cur.close()

    # Asegúrate de que el empleado fue añadido
    assert hid is not None, "El hotel no fue añadido correctamente"

    # Paso 2: Probar la eliminación del empleado mediante una petición DELETE
    delete_response = client.delete(f'/hotel/{hid}')
    assert delete_response.status_code == 200, "Fallo al eliminar hotel"

    # Opcional: Verificar que el empleado haya sido eliminado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM hotel WHERE hid = %s", (hid,))
        hotel = cur.fetchone()
        assert hotel is None, "El hotel no fue eliminado correctamente"
    finally:
        cur.close()
        db.close()



def test_put_hotel(client):
    # Insertar un empleado en la base de datos
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO hotel (chid, hname, hcity) 
            VALUES (%s, %s, %s) RETURNING hid""",
                    (5, "Hotel de Janiel", "Mayaguez"))
        hid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    # Asegurarse de que el empleado fue añadido
    assert hid is not None, "El hotel no fue añadido correctamente"

    # Actualizar el empleado a través de una petición PUT
    updated_hotel = {
        "chid": 4,
        "hname": "Hotel de Janiel actualizado",
        "hcity": "Mayaguez actualizado",
    }
    update_response = client.put(f'/hotel/{hid}', json=updated_hotel)
    assert update_response.status_code == 200, f"Fallo al actualizar hotel {update_response}"

    # Verificar que los cambios se aplicaron correctamente
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT chid, hname, hcity FROM hotel WHERE hid = %s", (hid,))
        hotel = cur.fetchone()
        assert hotel is not None, "El empleado no se encontró después de actualizar"
        assert hotel[0] == updated_hotel['chid'], "El chid del hotel no se actualizó correctamente"
        assert hotel[1] == updated_hotel['hname'], "El hname del hotel no se actualizó correctamente"
        assert hotel[2] == updated_hotel['hcity'], "La hcity del hotel no se actualizó correctamente"

    finally:
        cur.close()

    # Eliminar el empleado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM hotel WHERE hid = %s", (hid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()