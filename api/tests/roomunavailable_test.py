from api.model.db import Database
from datetime import datetime

def validate_room_unavailable_data(roomunavailable, expected_types):
    for key, expected_type in expected_types.items():
        assert key in roomunavailable, f"Expected key '{key}' not found in room data"
        assert isinstance(roomunavailable[key], expected_type), f"Expected type of '{key}' to be {expected_type.__name__}, got {type(roomunavailable[key]).__name__}"

    # Estructura de habitacion indisponible
    assert roomunavailable['ruid'] > 0, "Room unavailable ID should be greater than 0"
    assert roomunavailable['rid'] > 0, "Roo ID should be greater than 0 and should exist"
    assert isinstance(roomunavailable['startdate'], str), "Start date should be a string"
    assert isinstance(roomunavailable['enddate'], str), "End date should be a string"



def test_get_all_rooms_unavailable(client):
    expected_types = {
        'ruid': int,
        'rid': int,
        'startdate': str,
        'enddate': str
    }
    # Realizar una solicitud GET al endpoint /allroomsunavailable
    response = client.get('/roomunavailable')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    response_data = response.get_json()

    assert isinstance(response_data, list), "Expected list of unavailable rooms in the response"

    # Opcional: Prueba para verificar que la cantidad de habitaciones indisponible hay
    # expected_room_count = 4052 //Ajustar valor a la cantidad que hay en la base de datos
    # assert len(response_data) == expected_room_count, f"Expected {expected_room_count} unavailable rooms, but retrieved {len(response_data)}"

    #Verifica que el data type sea el correcto
    for room in response_data:
        for key, expected_type in expected_types.items():
            assert key in room, f"Expected key '{key}' not found in room data"
            assert isinstance(room[key], expected_type), f"Expected type of '{key}' to be {expected_type.__name__}, got {type(room[key]).__name__}"
def test_get_room_unavailable_by_id(client):
    expected_types = {
        'ruid': int,
        'rid': int,
        'startdate': str,
        'enddate': str
    }
    # Verifica que el id no se encuentre en la lista
    ruid = 55555
    response = client.get(f'/roomunavailable/{ruid}')
    assert response.status_code == 404, "Expected response code 404, got {response.status_code}"

    #Verifica que el id de la habitacion se encuentre en la lista
    ruid = 1
    response = client.get(f'/roomunavailable/{ruid}')
    assert response.status_code == 200, "Expected response code 200, got {response.status_code}"
    data = response.get_json()
    #Esa habitacion indisponible debe tener estructura de dictionary
    assert isinstance(data, dict), "Expected to be a dictionary"
    validate_room_unavailable_data(data, expected_types)
def test_post_room(client):
    employee_id = 9
    body = {"eid": employee_id}
    response = client.get(f'/roomunavailable', json=body)
    assert response.status_code == 200, "Employee 9 should not have authorization to add a room unavailable"

    # Empleado 4 tiene autorizacion
    new_roomunavailable = {
        "eid": 4,
        "rid": 1,
        "startdate": "2024-10-20",
        "enddate": "2024-10-30",
    }

    # Enviar petición POST al endpoint /hotel con los datos del empleado
    response = client.post('/roomunavailable', json=new_roomunavailable)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['status'] == "success", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM roomunavailable
                    WHERE rid = %s AND startdate = %s AND enddate = %s
                    """
        cur.execute(query, (new_roomunavailable['rid'], new_roomunavailable['startdate'], new_roomunavailable['enddate']))
        roomunavailable = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert roomunavailable is not None, "La habitacion indisponible añadida no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el hotel a eliminar
        query = """
                DELETE FROM roomunavailable
                WHERE rid = %s AND startdate = %s AND enddate = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (
            new_roomunavailable['rid'],
            new_roomunavailable['startdate'],
            new_roomunavailable['enddate']
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
        # Add a room unavailable to test deletion
        cur.execute("INSERT INTO roomunavailable (rid, startdate, enddate) VALUES (%s, %s, %s) RETURNING ruid", (1, "2024-11-20", "2024-11-30"))
        ruid = cur.fetchone()[0]
        db.conexion.commit()
    except Exception as e:
        print(f"Error al añadir habitacion para prueba de eliminación: {e}")
        db.conexion.rollback()
        assert False, f"Fallo al añadir habitacion para prueba de eliminación: {e}"
    finally:
        cur.close()

    assert ruid is not None, "La habitacion indisponible no fue añadida correctamente"
    # Delete room unavailable with the given id
    delete_response = client.delete(f'/roomunavailable/{ruid}')
    assert delete_response.status_code == 200, "Fallo al eliminar habitacion indisponible"

    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM roomunavailable WHERE ruid = %s", (ruid,))
        roomunavailable = cur.fetchone()
        # Verify that it was successfully deleted
        assert roomunavailable is None, "La habitacion no fue eliminada correctamente"
    finally:
        cur.close()
        db.close()


def test_put_room(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("INSERT INTO roomunavailable (rid, startdate, enddate) VALUES (%s, %s, %s) RETURNING ruid", (1, "2025-01-02", "2025-01-08"))
        ruid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    assert ruid is not None, "La habitacion indisponible no fue actualizda correctamente"

    # Actualizar la habitación a través de una petición PUT
    updated_roomunavailable = {
        "rid": 2,
        "startdate": "2022-01-02",
        "enddate": "2022-01-10"
    }
    update_response = client.put(f'/roomunavailable/{ruid}', json=updated_roomunavailable)
    assert update_response.status_code == 200, f"Fallo al actualizar la habitacion indisponible {update_response}"

    # Verificar que la habitación se haya actualizado correctamente
    updated_roomunavailable['ruid'] = ruid  # Añadir rid a los datos actualizados
    assert update_response.json['message'] == "Habitacion indisponible actualizada exitosamente", "Mensaje de actualización incorrecto"

    # Verificar que los cambios se aplicaron correctamente en la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT rid, startdate, enddate FROM roomunavailable WHERE ruid = %s", (ruid,))
        roomunavailable = cur.fetchone()
        assert roomunavailable is not None, "La habitacion indisponible no se encontró después de actualizar"
        assert roomunavailable[0] == updated_roomunavailable['rid'], "El id de la habaticion de la habitacion indisponible no se actualizó correctamente"
        assert str(roomunavailable[1]) == updated_roomunavailable['startdate'], "La fecha de comienzo de la habitacion indisponible no se actualizó correctamente"

        assert str(roomunavailable[2]) == updated_roomunavailable['enddate'], "La fecha de finalización de la habitación indisponible no se actualizó correctamente"

    finally:
        cur.close()

    # Eliminar la habitación de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM roomunavailable WHERE ruid = %s", (ruid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()
