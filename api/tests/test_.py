import pytest
from api.wsgi import create_app
from api.model.db import Database

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

    # Opcional: Verificar el mensaje de la respuesta
    response_data = response.get_json()
    assert response_data['message'] == "Empleado agregado exitosamente", "Expected success message in the response"

    #consulta a la base de datos
    # response = client.get('/employee')
    # employees = response.get_json()
    # # Buscar el empleado recién añadido en la lista
    # employee_found = any(
    #     employee['fname'] == new_employee['fname'] and
    #     employee['lname'] == new_employee['lname'] and
    #     employee['age'] == new_employee['age'] and
    #     employee['salary'] == new_employee['salary'] and
    #     employee['position'] == new_employee['position']
    #     for employee in employees
    # )
    #
    # assert employee_found, "El empleado añadido no se encontró en la lista de empleados"


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
