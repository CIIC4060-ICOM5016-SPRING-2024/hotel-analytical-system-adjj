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




def test_post_login(client):  # Assuming 'db' is a fixture or a parameter that provides database access
    # New employee data
    new_employee = {
        "hid": 17,
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "salary": 18000,
        "position": "Regular"
    }

    # New login data (without the 'eid')
    new_login = {
        "username": "newuser",
        "password": "newpass"
    }

    # Create a new employee
    employee_response = client.post('/employee', json=new_employee)
    assert employee_response.status_code == 201, "Expected status code 201 but got {}".format(employee_response.status_code)

    # Fetch the 'eid' from the database based on 'fname' and 'lname'
    db = Database()

    cur = db.conexion.cursor()
    query = "SELECT eid FROM employee WHERE fname = %s AND lname = %s ORDER BY eid DESC LIMIT 1"
    cur.execute(query, (new_employee['fname'], new_employee['lname']))
    employee = cur.fetchone()
    assert employee is not None, "Failed to find the newly created employee in the database"
    new_login['eid'] = employee[0]  # Assuming the first column in the SELECT is 'eid'

    # Create a login for the new employee
    login_response = client.post('/login', json=new_login)
    assert login_response.status_code == 201, "Expected status code 201 but got {}".format(login_response.status_code)

    login_response_data = login_response.get_json()
    assert login_response_data['status'] == "success", "Expected success message in the response"

    # Cleanup: Remove the test login and employee from the database
    try:
        cur.execute("DELETE FROM login WHERE eid = %s", (new_login['eid'],))
        cur.execute("DELETE FROM employee WHERE eid = %s", (new_login['eid'],))
        db.conexion.commit()
    finally:
        cur.close()

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

# def test_put_login(client):
#     db = Database()
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("""SELECT lid, eid, username, password FROM login""")
#         lid = cur.fetchone()[0]
#         db.conexion.commit()
#     finally:
#         cur.close()
#
#     assert lid is not None, "El Login no fue añadido correctamente"
#
#     updated_login = {
#         "eid": 1,
#         "username": "cbonhome0 actualizado",
#         "password": "tS6M@Qnt actualizado"
#     }
#     update_response = client.put(f'/login/{lid}', json=updated_login)
#     assert update_response.status_code == 200, f"Fallo al actualizar login {update_response}"
#
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("SELECT eid, username, password FROM login WHERE lid = %s", (lid,))
#         login = cur.fetchone()
#         assert login is not None, "El Login no se encontró después de actualizar"
#         assert login[0] == updated_login['eid'], "El eid del login no se actualizó correctamente"
#         assert login[1] == updated_login['username'], "El username del login no se actualizó correctamente"
#         assert login[2] == updated_login['password'], "La password del login no se actualizó correctamente"
#
#     finally:
#         cur.close()
#
#     rollback_updated_login = {
#         "eid": 1,
#         "username": "cbonhome0",
#         "password": "tS6M@Qnt"
#     }
#     rollback_update_response = client.put(f'/login/{lid}', json=rollback_updated_login)
#     assert rollback_update_response.status_code == 200, f"Fallo al actualizar login {rollback_update_response}"
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("SELECT eid, username, password FROM login WHERE lid = %s", (lid,))
#         login = cur.fetchone()
#         assert login is not None, "El Login no se encontró después de actualizar"
#         assert login[0] == rollback_updated_login['eid'], "El eid del login no se actualizó correctamente"
#         assert login[1] == rollback_updated_login['username'], "El username del login no se actualizó correctamente"
#         assert login[2] == rollback_updated_login['password'], "La password del login no se actualizó correctamente"
#     finally:
#         cur.close()


# def test_put_login(client):
#     db = Database()
#     lid = None
#     try:
#         cur = db.conexion.cursor()
#         # Fetch the first login entry to update. Ensure this entry's eid is unique or suitable for your test case.
#         cur.execute("""SELECT lid FROM login LIMIT 1""")
#         result = cur.fetchone()
#         if result:
#             lid = result[0]
#         else:
#             assert False, "No login entries found for testing"
#     finally:
#         cur.close()
#
#     updated_login = {
#         # Ensure this 'eid' refers to the same employee associated with the 'lid' fetched above
#         "eid": 1,
#         "username": "cbonhome0 actualizado",
#         "password": "tS6M@Qnt actualizado"
#     }
#     update_response = client.put(f'/login/{lid}', json=updated_login)
#     assert update_response.status_code == 200, f"Failed to update login: {update_response}"
#
#     # Verification and rollback logic remains the same, ensuring that 'eid' does not violate the unique constraint




def test_put_login(client):
    # Existing login details
    lid = 1
    eid = 1
    original_login = {
        "username": "cbonhome0",
        "password": "tS6M@Qnt"
    }

    # Updated login details for the test
    updated_login = {
        "eid": eid,  # Use the same eid since it's an existing login
        "username": "UpdatedUser",
        "password": "UpdatedPass123"
    }

    # Attempt to update the login through a PUT request
    update_response = client.put(f'/login/{lid}', json=updated_login)
    assert update_response.status_code == 200, "Failed to update login"

    # Verify the updates were applied successfully
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT eid, username, password FROM login WHERE lid = %s", (lid,))
        login = cur.fetchone()
        assert login is not None, "Login not found after update"
        assert login[1] == updated_login['username'], "Username did not update correctly"
        assert login[2] == updated_login['password'], "Password did not update correctly"
    finally:
        cur.close()

    # Rollback to the original login data after the test
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            UPDATE login SET username = %s, password = %s WHERE lid = %s
        """, (original_login['username'], original_login['password'], lid))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()

    # Optionally, you can add an assertion here to check if the rollback was successful

