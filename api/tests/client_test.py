from api.model.db import Database


def test_get_client_by_id(client):

    for clid in range(1,401):
        response = client.get(f'/client/{clid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"

        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'fname' in data, "'hid' debe estar presente"
        assert 'lname' in data, "'fname' debe estar presente"
        assert 'age' in data, "'lname' debe estar presente"
        assert 'memberyear' in data, "'position' debe estar presente"
        assert isinstance(data['fname'], str), "fname debe ser un cadena"
        assert isinstance(data['lname'], str), "lname debe ser un cadena"
        assert isinstance(data['age'], int), f"age debe ser una entero"
        assert isinstance(data['memberyear'], int), f"memberyear debe ser una entero"

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

def test_post_client(client):
    # Datos del nuevo empleado
    new_client = {
    "fname": "Janiel",
    "lname": "Núñez",
    "age": 21,
    "memberyear": "2020"
    }

    # Enviar petición POST al endpoint /employee con los datos del empleado
    response = client.post('/client', json=new_client)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['message'] == "Client agregado exitosamente", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM client 
                    WHERE fname = %s AND lname = %s AND age = %s AND memberyear = %s
                    """
        cur.execute(query, (new_client['fname'], new_client['lname'], new_client['age'], new_client['memberyear']))
        client__ = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert client__ is not None, "El client añadido no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el empleado a eliminar
        query = """
                DELETE FROM client
                WHERE fname = %s AND lname = %s AND age = %s AND memberyear = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (
            new_client['fname'],
            new_client['lname'],
            new_client['age'],
            new_client['memberyear'],
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

def test_delete_client(client):
    # Paso 1: Añadir un nuevo empleado directamente a la base de datos y obtener su eid
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO client (fname, lname, age, memberyear) 
            VALUES (%s, %s, %s, %s) RETURNING clid""",
                    ("Janiel", "Núñez", 21, 2020))
        clid = cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro
        db.conexion.commit()
    except Exception as e:
        print(f"Error al añadir client para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir client para prueba de eliminación"
    finally:
        cur.close()

    # Asegúrate de que el empleado fue añadido
    assert clid is not None, "El client no fue añadido correctamente"

    # Paso 2: Probar la eliminación del client mediante una petición DELETE
    delete_response = client.delete(f'/client/{clid}')
    assert delete_response.status_code == 200, "Fallo al eliminar client"

    # Opcional: Verificar que el client haya sido eliminado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM client WHERE clid = %s", (clid,))
        client__ = cur.fetchone()
        assert client__ is None, "El client no fue eliminado correctamente"
    finally:
        cur.close()
        db.close()

def test_put_client(client):
    # Insertar un empleado en la base de datos
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO client (fname, lname, age, memberyear) 
            VALUES (%s, %s, %s, %s) RETURNING clid""",
                    ("Janiel", "Núñez", 21, 2020))
        clid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    # Asegurarse de que el empleado fue añadido
    assert clid is not None, "El client no fue añadido correctamente"

    # Actualizar el client a través de una petición PUT
    updated_client = {
        "fname": "Janiel Updated",
        "lname": "Núñez Updated",
        "age": 22,
        "memberyear": 2023,
    }
    update_response = client.put(f'/client/{clid}', json=updated_client)
    assert update_response.status_code == 200, "Fallo al actualizar client"

    # Verificar que los cambios se aplicaron correctamente
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT fname, lname, age, memberyear FROM client WHERE clid = %s", (clid,))
        client__ = cur.fetchone()
        assert client__ is not None, "El empleado no se encontró después de actualizar"
        assert client__[0] == updated_client['fname'], "El nombre del client no se actualizó correctamente"
        assert client__[1] == updated_client['lname'], "El apellido del client no se actualizó correctamente"
        assert client__[2] == updated_client['age'], "La edad del client no se actualizó correctamente"
        assert client__[3] == updated_client['memberyear'], "El memberyear del client no se actualizó correctamente"
    finally:
        cur.close()

    # Eliminar el empleado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM client WHERE clid = %s", (clid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()
