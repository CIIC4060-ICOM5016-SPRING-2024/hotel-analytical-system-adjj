from api.model.db import Database


def test_get_all_logins(client):
    response = client.get('/login')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:
        for i in range(len(data)):
            assert 'lid' in data[i], "lid has to be a key"
            assert 'eid' in data[i], "eid has to be a key"
            assert 'username' in data[i], "username has to be a key"
            assert 'password' in data[i], "password has to be a key"
            assert isinstance(data[i]['lid'], int), f"lid has to be integer but got {type(data[i]['lid'])}"
            assert isinstance(data[i]['eid'], int), f"eid has to be integer but got {type(data[i]['eid'])}"
            assert isinstance(data[i]['username'], str), f"fname has to be string but got {type(data[i]['username'])}"
            assert isinstance(data[i]['password'], str), f"lname has to be string but got {type(data[i]['password'])}"


def test_get_login_by_id(client):
    for lid in range(1, 200):
        response = client.get(f'/login/{lid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"

        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        assert 'lid' in data, "'lid' debe estar presente"
        assert 'eid' in data, "'eid'  debe estar presente"
        assert 'username' in data, "'username'  debe estar presente"
        assert 'password' in data, "'password'  debe estar presente"
        assert isinstance(data['lid'], int), "lid debe ser un integer"
        assert isinstance(data['eid'], int), "eid debe ser un integer"
        assert isinstance(data['username'], str), "username debe ser una string"
        assert isinstance(data['password'], str), "password debe ser una string"

def test_post_login(client):

    return




def test_delete_login(client):
    # Paso 1: Añadir un nuevo empleado directamente a la base de datos y obtener su eid
    db = Database()
    try:
        cur = db.conexion.cursor()

        cur.execute("""
            INSERT INTO employee (hid, fname, lname, age, salary, position) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING eid""",
                    (17, "Jandel", "Rodriguez", 21, 18000, "Regular"))

        eid = cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro
        db.conexion.commit()

         # Asume que INSERT...RETURNING retorna el eid del nuevo registro
        db.conexion.commit()

    except Exception as e:
        print(f"Error al añadir login para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir login para prueba de eliminación"
    finally:
        cur.close()
    try:
        cur2 = db.conexion.cursor()

        cur2.execute("""
            INSERT INTO login (eid, username, password)
            VALUES (%s, %s, %s) RETURNING lid""",
                    (eid, "Jandel", "abcdefg"))

        lid = cur2.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro
        db.conexion.commit()

    except Exception as e:
        print(f"Error al añadir login para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir login para prueba de eliminación"
    finally:
        cur2.close()


    # Asegúrate de que el empleado fue añadido
    assert lid is not None, "El login no fue añadido correctamente"

    # Paso 2: Probar la eliminación del empleado mediante una petición DELETE
    delete_response = client.delete(f'/login/{lid}')
    assert delete_response.status_code == 200, "Fallo al eliminar login"

    # Opcional: Verificar que el empleado haya sido eliminado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM login WHERE lid = %s", (lid,))
        employee = cur.fetchone()
        assert employee is None, "El login no fue eliminado correctamente"
    finally:
        cur.close()


    # Asegúrate de que el empleado fue añadido
    assert eid is not None, "El empleado no fue añadido correctamente"

    # Paso 2: Probar la eliminación del empleado mediante una petición DELETE
    delete_response = client.delete(f'/employee/{eid}')
    assert delete_response.status_code == 200, "Fallo al eliminar empleado"

    # Opcional: Verificar que el empleado haya sido eliminado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM employee WHERE eid = %s", (eid,))
        employee = cur.fetchone()
        assert employee is None, "El empleado no fue eliminado correctamente"
    finally:
        cur.close()
        db.close()

def test_put_login(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""SELECT lid, eid, username, password FROM login""")
        lid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    assert lid is not None, "El Login no fue añadido correctamente"

    updated_login = {
        "eid": 1,
        "username": "cbonhome0 actualizado",
        "password": "tS6M@Qnt actualizado"
    }
    update_response = client.put(f'/login/{lid}', json=updated_login)
    assert update_response.status_code == 200, f"Fallo al actualizar login {update_response}"

    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT eid, username, password FROM login WHERE lid = %s", (lid,))
        login = cur.fetchone()
        assert login is not None, "El Login no se encontró después de actualizar"
        assert login[0] == updated_login['eid'], "El eid del login no se actualizó correctamente"
        assert login[1] == updated_login['username'], "El username del login no se actualizó correctamente"
        assert login[2] == updated_login['password'], "La password del login no se actualizó correctamente"

    finally:
        cur.close()

    rollback_updated_login = {
        "eid": 1,
        "username": "cbonhome0",
        "password": "tS6M@Qnt"
    }
    rollback_update_response = client.put(f'/login/{lid}', json=rollback_updated_login)
    assert rollback_update_response.status_code == 200, f"Fallo al actualizar login {rollback_update_response}"
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT eid, username, password FROM login WHERE lid = %s", (lid,))
        login = cur.fetchone()
        assert login is not None, "El Login no se encontró después de actualizar"
        assert login[0] == rollback_updated_login['eid'], "El eid del login no se actualizó correctamente"
        assert login[1] == rollback_updated_login['username'], "El username del login no se actualizó correctamente"
        assert login[2] == rollback_updated_login['password'], "La password del login no se actualizó correctamente"
    finally:
        cur.close()





