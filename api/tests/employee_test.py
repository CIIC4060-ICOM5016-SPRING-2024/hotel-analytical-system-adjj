from api.model.db import Database

def test_get_employee_by_id(client):

    for eid in range(1,201):
        response = client.get(f'/employee/{eid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code} y eid={eid}"

        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'hid' in data, "'hid' debe estar presente"
        assert 'fname' in data, "'fname' debe estar presente"
        assert 'lname' in data, "'lname' debe estar presente"
        assert 'position' in data, "'position' debe estar presente"
        assert 'salary' in data, "'salary' debe estar presente"
        assert 'age' in data, "'age' debe estar presente"
        assert isinstance(data['hid'], int), "hid debe ser un entero"
        assert isinstance(data['fname'], str), "fname debe ser un entero"
        assert isinstance(data['lname'], str), f"lname debe ser una cadena"
        assert isinstance(data['position'], str), f"position debe ser una cadena pero se obtuvo {type(data['position'])}"
        assert isinstance(data['salary'], float), "salary debe ser un float"
        assert isinstance(data['age'], int), "age debe ser un entero"
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
def test_post_employee(client):
    # Datos del nuevo empleado
    new_employee = {
        "hid": 17,
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "salary": 18000,
        "position": "Regular"
    }

    # Enviar petición POST al endpoint /employee con los datos del empleado
    response = client.post('/employee', json=new_employee)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['message'] == "Empleado agregado exitosamente", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM employee 
                    WHERE fname = %s AND lname = %s AND age = %s AND salary = %s AND position = %s
                    """
        cur.execute(query, (new_employee['fname'], new_employee['lname'], new_employee['age'], new_employee['salary'],
                            new_employee['position']))
        employee = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert employee is not None, "El empleado añadido no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el empleado a eliminar
        query = """
                DELETE FROM employee
                WHERE hid = %s AND fname = %s AND lname = %s AND age = %s AND salary = %s AND position = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (
            new_employee['hid'],
            new_employee['fname'],
            new_employee['lname'],
            new_employee['age'],
            new_employee['salary'],
            new_employee['position'],
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

def test_delete_employee(client):
    # Paso 1: Añadir un nuevo empleado directamente a la base de datos y obtener su eid
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO employee (hid, fname, lname, age, salary, position) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING eid""",
                    (17, "Janiel", "Núñez", 21, 18000, "Regular"))
        eid = cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro
        db.conexion.commit()
    except Exception as e:
        print(f"Error al añadir empleado para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, "Fallo al añadir empleado para prueba de eliminación"
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

def test_put_employee(client):
    # Insertar un empleado en la base de datos
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO employee (hid, fname, lname, age, salary, position) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING eid""",
                    (17, "Janiel", "Núñez", 21, 18000, "Regular"))
        eid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    # Asegurarse de que el empleado fue añadido
    assert eid is not None, "El empleado no fue añadido correctamente"

    # Actualizar el empleado a través de una petición PUT
    updated_employee = {
        "hid": 17,
        "fname": "Janiel Updated",
        "lname": "Núñez Updated",
        "age": 22,
        "salary": 19000,
        "position": "Regular"
    }
    update_response = client.put(f'/employee/{eid}', json=updated_employee)
    assert update_response.status_code == 200, "Fallo al actualizar empleado"

    # Verificar que los cambios se aplicaron correctamente
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT hid, fname, lname, age, salary, position FROM employee WHERE eid = %s", (eid,))
        employee = cur.fetchone()
        assert employee is not None, "El empleado no se encontró después de actualizar"
        assert employee[1] == updated_employee['fname'], "El nombre del empleado no se actualizó correctamente"
        assert employee[2] == updated_employee['lname'], "El apellido del empleado no se actualizó correctamente"
        assert employee[3] == updated_employee['age'], "La edad del empleado no se actualizó correctamente"
        assert employee[4] == updated_employee['salary'], "El salario del empleado no se actualizó correctamente"
        assert employee[5] == updated_employee['position'], "La posición del empleado no se actualizó correctamente"
    finally:
        cur.close()

    # Eliminar el empleado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM employee WHERE eid = %s", (eid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()