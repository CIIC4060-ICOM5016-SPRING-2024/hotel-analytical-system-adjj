from api.model.db import Database


def test_get_all_room_descriptions(client):
    response = client.get('/roomdescription')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'rdid' in data[i], "rdid has to be a key"
            assert 'rname' in data[i], "rname has to be a key"
            assert 'rtype' in data[i], "hname has to be a key"
            assert 'capacity' in data[i], "capacity has to be a key"
            assert 'ishandicap' in data[i], "ishandicap has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['rdid'], int), f"rdid has to be int but got {type(data[i]['rdid'])}"
            assert isinstance(data[i]['rname'], str), f"rname has to be str but got {type(data[i]['rname'])}"
            assert isinstance(data[i]['rtype'], str), f"rtype has to be str but got {type(data[i]['rtype'])}"
            assert isinstance(data[i]['capacity'], int), f"capacity has to be int but got {type(data[i]['capacity'])}"
            assert isinstance(data[i]['ishandicap'],
                              bool), f"ishandicap has to be bool but got {type(data[i]['ishandicap'])}"


def test_get_room_descriptions_by_id(client):
    # Asumiendo que ya tienes un hotel en tu base de datos de prueba, utiliza ese ID. De lo contrario, inserta uno y obtén el ID.
    # Reemplaza esto con un ID válido de tu base de datos de prueba o después de insertar un hotel nuevo
    for rdid in range(1, 62):
        response = client.get(f'/roomdescription/{rdid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"

        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'rdid' in data, "'rdid' debe estar presente"
        assert 'rname' in data, "'rname' debe estar presente"
        assert 'rtype' in data, "'rtype' debe estar presente"
        assert 'capacity' in data, "'capacity' debe estar presente"
        assert 'ishandicap' in data, "'ishandicap' debe estar presente"

        assert isinstance(data['rdid'], int), "rdid debe ser un entero"
        assert isinstance(data['rname'], str), "rname debe ser un str"
        assert isinstance(data['rtype'], str), "rtype debe ser un str"
        assert isinstance(data['capacity'], int), "capacity debe ser una int"
        assert isinstance(data['ishandicap'], bool), "ishandicap debe ser un bool"


def test_post_room_description(client):
    # Details of the new room
    new_roomdescription = {
        "rname": "Standard Queen",
        "rtype": "Premium",
        "capacity": 2,
        "ishandicap": False  # or True, depending on the test scenario
    }

    # Send POST request to the /roomdescription endpoint with the room details
    response = client.post('/roomdescription', json=new_roomdescription)

    # Verify that the response status code is 201 (Created)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['status'] == "success", "Expected success message in the response"

    db = Database()
    # Direct query to the database to ensure the room was added
    try:
        cur = db.conexion.cursor()
        query = """
                SELECT * FROM roomdescription 
                WHERE rname = %s AND rtype = %s AND capacity = %s AND ishandicap = %s 
                """
        cur.execute(query, (new_roomdescription['rname'], new_roomdescription['rtype'], new_roomdescription['capacity'],
                            new_roomdescription['ishandicap']))
        roomdescription = cur.fetchone()  # Use fetchone() to get the first matching result
        assert roomdescription is not None, "The added room description was not found in the database"
    finally:
        cur.close()

    # Direct query to the database to delete the added room
    try:
        cur = db.conexion.cursor()
        # Construct the DELETE query using all fields to specify the room to delete
        query = """
                DELETE FROM roomdescription
                WHERE rname = %s AND rtype = %s AND capacity = %s AND ishandicap = %s
                """
        # Prepare the values to use in the DELETE query
        values = (
            new_roomdescription['rname'],
            new_roomdescription['rtype'],
            new_roomdescription['capacity'],
            new_roomdescription['ishandicap'],

        )
        # Execute the DELETE query
        cur.execute(query, values)
        # Commit the changes
        db.conexion.commit()
    except Exception as e:
        print(f"Error cleaning up the database: {e}")
        db.conexion.rollback()
    finally:
        # Ensure to close the cursor
        cur.close()
    db.close()


def test_delete_roomdescription(client):
    # Paso 1: Añadir un nuevo empleado directamente a la base de datos y obtener su eid
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO roomdescription (rname, rtype, capacity, ishandicap) 
            VALUES (%s, %s, %s, %s) RETURNING rdid""",
                    ("Standard", "Basic", 1, False))
        rdid = cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro
        db.conexion.commit()
    except Exception as e:
        print(f"Error al añadir room description para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir room description para prueba de eliminación"
    finally:
        cur.close()

    # Asegúrate de que el empleado fue añadido
    assert rdid is not None, "El room description no fue añadido correctamente"

    # Paso 2: Probar la eliminación del empleado mediante una petición DELETE
    delete_response = client.delete(f'/roomdescription/{rdid}')
    assert delete_response.status_code == 200, "Fallo al eliminar room description"
    #
    # Opcional: Verificar que el empleado haya sido eliminado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM roomdescription WHERE rdid = %s", (rdid,))
        roomdescription = cur.fetchone()
        assert roomdescription is None, "El room description no fue eliminado correctamente"
    finally:
        cur.close()
        db.close()

def test_put_roomdescription(client):
    # Insertar un empleado en la base de datos
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO roomdescription (rname, rtype, capacity,ishandicap)
            VALUES (%s, %s, %s, %s) RETURNING rdid""",
                    ("Standard King", "Deluxe",2,True))
        rdid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    # Asegurarse de que el empleado fue añadido
    assert rdid is not None, "La descripcion de habitacion no fue añadida correctamente"

    # Actualizar el empleado a través de una petición PUT
    updated_roomdescription = {
        "rname": "Standard",
        "rtype": "Basic",
        "capacity": 1,
        "ishandicap": False
    }
    update_response = client.put(f'/roomdescription/{rdid}', json=updated_roomdescription)
    assert update_response.status_code == 200, f"Fallo al actualizar descripcion de la habitacion {update_response}"

    # Verificar que los cambios se aplicaron correctamente
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT rname, rtype, capacity,ishandicap FROM roomdescription WHERE rdid = %s", (rdid,))
        roomdescription = cur.fetchone()
        assert roomdescription is not None, "El empleado no se encontró después de actualizar"
        assert roomdescription[0] == updated_roomdescription['rname'], "El nombre del cuarto no se actualizó correctamente"
        assert roomdescription[1] == updated_roomdescription['rtype'], "El tipo del cuarto no se actualizó correctamente"
        assert roomdescription[2] == updated_roomdescription['capacity'], "La capacidad del cuarto no se actualizó correctamente"
        assert roomdescription[3] == updated_roomdescription['ishandicap'], "handicap del cuarto no se actualizó correctamente"


    finally:
        cur.close()

    # Eliminar el empleado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM roomdescription WHERE rdid = %s", (rdid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()
