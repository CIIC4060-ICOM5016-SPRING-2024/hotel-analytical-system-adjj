from api.model.db import Database

def validate_room_data(room, expected_types):
    for key, expected_type in expected_types.items():
        assert key in room, f"Expected key '{key}' not found in room data"
        assert isinstance(room[key], expected_type), f"Expected type of '{key}' to be {expected_type.__name__}, got {type(room[key]).__name__}"
    # Lo4gica de la estructura de las habitaciones en la base de datos
    assert room['rid'] > 0, "Room ID should be greater than 0"
    assert room['hid'] > 0, "Hotel ID should be greater than 0"
    assert room['rdid'] > 0, "Room Description ID should be greater than 0"
    assert room['rprice'] >= 0, "Room price should be non-negative"

def test_get_all_rooms(client):
    response = client.get('/room')
    assert response.status_code == 200, f"Expected response code 200, got {response.status_code}"
    data = response.get_json()
    #Debe ser una lista
    assert isinstance(data, list), "Expected to be a list"

    #Data types
    expected_types = {
        'rid': int,
        'hid': int,
        'rdid': int,
        'rprice': float
    }

    for room in data:
        validate_room_data(room, expected_types)

def test_get_room_by_id(client):
    expected_types = {
        'rid': int,
        'hid': int,
        'rdid': int,
        'rprice': float
    }
    #Verifica que el id de la habitacion se encuentre en la lista
    for rid in range(1, 451):
        response = client.get(f'/room/{rid}')
        assert response.status_code == 200, "Expected response code 200, got {response.status_code}"
        data = response.get_json()
        #Esa habitacion debe tener estructura de dictionary
        assert isinstance(data, dict), "Expected to be a dictionary"
        validate_room_data(data, expected_types)

def test_post_room(client):
    # Datos del nuevo empleado
    new_room = {
        "hid": 1,
        "rdid": 10,
        "rprice": 100.50,
    }

    # Enviar petición POST al endpoint /hotel con los datos del empleado
    response = client.post('/room', json=new_room)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['status'] == "success", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM room 
                    WHERE hid = %s AND rdid = %s AND rprice = %s
                    """
        cur.execute(query, (new_room['hid'], new_room['rdid'], new_room['rprice']))
        room = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert room is not None, "La habitacion añadida no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el hotel a eliminar
        query = """
                DELETE FROM room
                WHERE hid = %s AND rdid = %s AND rprice = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (
            new_room['hid'],
            new_room['rdid'],
            new_room['rprice']
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

def test_room_delete(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        #Añade habitacion para comprobar que se puede eliminar
        cur.execute("INSERT INTO room (hid, rdid, rprice) VALUES (%s, %s, %s) RETURNING rid", (1, 10, 100.50))
        rid = cur.fetchone()[0]
        db.conexion.commit()
    except Exception as e:
        print(f"Error al añadir habitacion para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir habitacion para prueba de eliminación"
    finally:
        cur.close()

    assert rid is not None, "La habitacion no fue añadida correctamente"
    #Elimina habitacion con el id dado
    delete_response = client.delete(f'/room/{rid}')
    assert delete_response.status_code == 200, "Fallo al eliminar habitacion"

    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM room WHERE rid = %s", (rid,))
        room = cur.fetchone()
        #Verifica que se haya eliminado correctamente
        assert room is None, "La habitacion no fue eliminada correctamente"
    finally:
        cur.close()
        db.close()


def test_put_room(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("INSERT INTO room (hid, rdid, rprice) VALUES (%s, %s, %s) RETURNING rid", (1, 10, 100.50))
        rid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    assert rid is not None, "La habitacion no fue actualizda correctamente"

    # Actualizar la habitación a través de una petición PUT
    updated_room = {
        "hid": 2,
        "rdid": 11,
        "rprice": 100.55
    }
    update_response = client.put(f'/room/{rid}', json=updated_room)
    assert update_response.status_code == 200, f"Fallo al actualizar la habitacion {update_response}"

    # Verificar que la habitación se haya actualizado correctamente
    updated_room['rid'] = rid  # Añadir rid a los datos actualizados
    assert update_response.json['message'] == "Habitacion actualizada exitosamente", "Mensaje de actualización incorrecto"

    # Verificar que los cambios se aplicaron correctamente en la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT hid, rdid, rprice FROM room WHERE rid = %s", (rid,))
        room = cur.fetchone()
        assert room is not None, "La habitacion no se encontró después de actualizar"
        assert room[0] == updated_room['hid'], "El id del hotel de la habitacion no se actualizó correctamente"
        assert room[1] == updated_room['rdid'], "El id de la descripcion de la habitacion no se actualizó correctamente"
        assert room[2] == updated_room['rprice'], "El precio de la habitacion no se actualizó correctamente"

    finally:
        cur.close()

    # Eliminar la habitación de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM room WHERE rid = %s", (rid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()

def test_post_room_with_missing_fields(client):
    # Datos de la habitación con un dato faltante
    new_room_missing_field = {
        "hid": 1,
        # "rdid": 10, Este campo se omite intencionalmente
        "rprice": 100.50,
    }

    response = client.post('/room', json=new_room_missing_field)

    # Verificar que la respuesta tenga un código de estado 400 (Bad Request)
    assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['status'] == "error", "Expected error message in the response"