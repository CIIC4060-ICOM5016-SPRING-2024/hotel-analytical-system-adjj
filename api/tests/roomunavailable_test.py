# from api.model.db import Database
#
# from datetime import datetime
#
# def validate_roomunavailable_data(roomunavailable, expected_types):
#     for key, expected_type in expected_types.items():
#         assert key in roomunavailable, f"Expected key '{key}' not found in room data"
#         assert isinstance(roomunavailable[key], expected_type), f"Expected type of '{key}' to be {expected_type.__name__}, got {type(roomunavailable[key]).__name__}"
#
#     # Estructura de habitacion indisponible
#     assert roomunavailable['ruid'] > 0, "Room unavailable ID should be greater than 0"
#     assert roomunavailable['rid'] > 0, "Roo ID should be greater than 0 and should exist"
#
#     # Verificar el formato de las fechas startdate y enddate
#     try:
#         start_date = datetime.strptime(roomunavailable['startdate'], '%Y-%m-%d')
#         end_date = datetime.strptime(roomunavailable['enddate'], '%Y-%m-%d')
#     except ValueError:
#         raise AssertionError("startdate and enddate must be in YYYY-MM-DD format")
#
#     # Asegurarse de que startdate es <= enddate
#     assert start_date <= end_date, "startdate must be less than or equal to enddate"
#
#
# def test_get_all_rooms(client):
#     response = client.get('/roomunavailable')
#     assert response.status_code == 200, f"Expected response code 200, got {response.status_code}"
#     data = response.get_json()
#     #Debe ser una lista
#     assert isinstance(data, list), "Expected to be a list"
#
#     #Data types
#     expected_types = {
#         'ruid': int,
#         'rid': int,
#         'startdate': str,
#         'enddate': str
#     }
#
#     for roomunavailable in data:
#         validate_roomunavailable_data(roomunavailable, expected_types)
#
# def test_get_room_by_id(client):
#     expected_types = {
#         'ruid': int,
#         'rid': int,
#         'startdate': int,
#         'enddate': float
#     }
#     #Verifica que el id de la habitacion se encuentre en la lista
#     for ruid in range(1, 4052):
#         response = client.get(f'/roomunavailable/{ruid}')
#         assert response.status_code == 200, "Expected response code 200, got {response.status_code}"
#         data = response.get_json()
#         #Esa habitacion debe tener estructura de dictionary
#         assert isinstance(data, dict), "Expected to be a dictionary"
#         validate_roomunavailable_data(data, expected_types)
#
# def test_post_room(client):
#     # Datos del nuevo empleado
#     new_roomunavailable = {
#         "rid": 1,
#         "startdate": 10,
#         "enddate": 100.50,
#     }
#
#     # Enviar petición POST al endpoint /hotel con los datos del empleado
#     response = client.post('/roomunavailable', json=new_roomunavailable)
#
#     # Verificar que la respuesta tenga un código de estado 201 (creado)
#     assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
#
#     response_data = response.get_json()
#     assert response_data['message'] == "Habitacion agregada exitosamente", "Expected success message in the response"
#
#     db = Database()
#     #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
#     try:
#         cur = db.conexion.cursor()
#         query = """
#                     SELECT * FROM roomunavailable
#                     WHERE rid = %s AND startdate = %s AND enddate = %s
#                     """
#         cur.execute(query, (new_roomunavailable['hid'], new_roomunavailable['rdid'], new_roomunavailable['rprice']))
#         roomunavailable = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
#         assert roomunavailable is not None, "La habitacion añadida no se encontró en la base de datos"
#     finally:
#         cur.close()
#
#     #Consulta directa con la base para borrar el elemento añadido
#     try:
#         cur = db.conexion.cursor()
#         # Construye la consulta DELETE utilizando todos los campos para especificar el hotel a eliminar
#         query = """
#                 DELETE FROM roomunavailable
#                 WHERE rid = %s AND startdate = %s AND enddate = %s
#                 """
#         # Preparar los valores a utilizar en la consulta DELETE
#         values = (
#             new_roomunavailable['rid'],
#             new_roomunavailable['startdate'],
#             new_roomunavailable['enddate']
#         )
#         # Ejecutar la consulta DELETE
#         cur.execute(query, values)
#         # Hacer commit de los cambios
#         db.conexion.commit()
#     except Exception as e:
#         print(f"Error al limpiar la base de datos: {e}")
#         db.conexion.rollback()
#     finally:
#         # Asegurarse de cerrar el cursor y la conexión
#         cur.close()
#     db.close()
#
# def test_room_delete(client):
#     db = Database()
#     try:
#         cur = db.conexion.cursor()
#         #Añade habitacion para comprobar que se puede eliminar
#         cur.execute("INSERT INTO roomunavailable (rid, startdate, enddate) VALUES (%s, %s, %s) RETURNING ruid", (1, 10, 100.50))
#         ruid = cur.fetchone()[0]
#         db.conexion.commit()
#     except Exception as e:
#         print(f"Error al añadir habitacion para prueba de eliminación: {e}")
#         db.conexion.rollback()
#         assert False, "Fallo al añadir habitacion para prueba de eliminación"
#     finally:
#         cur.close()
#
#     assert ruid is not None, "La habitacion no fue añadida correctamente"
#     #Elimina habitacion con el id dado
#     delete_response = client.delete(f'/roomunavailable/{ruid}')
#     assert delete_response.status_code == 200, "Fallo al eliminar habitacion"
#
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("SELECT * FROM roomunavailable WHERE ruid = %s", (ruid,))
#         room = cur.fetchone()
#         #Verifica que se haya eliminado correctamente
#         assert room is None, "La habitacion no fue eliminada correctamente"
#     finally:
#         cur.close()
#         db.close()
#
#
# def test_put_room(client):
#     db = Database()
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("INSERT INTO room (rid, startdate, enddate) VALUES (%s, %s, %s) RETURNING ruid", (1, 10, 100.50))
#         ruid = cur.fetchone()[0]
#         db.conexion.commit()
#     finally:
#         cur.close()
#
#     assert ruid is not None, "La habitacion no fue actualizda correctamente"
#
#     # Actualizar la habitación a través de una petición PUT
#     updated_roomunavailable = {
#         "rid": 2,
#         "startdate": 11,
#         "endddate": 100.55
#     }
#     update_response = client.put(f'/roomunavailable/{ruid}', json=updated_roomunavailable)
#     assert update_response.status_code == 200, f"Fallo al actualizar la habitacion {update_response}"
#
#     # Verificar que la habitación se haya actualizado correctamente
#     updated_roomunavailable['ruid'] = ruid  # Añadir rid a los datos actualizados
#     assert update_response.json['message'] == "Habitacion actualizada exitosamente", "Mensaje de actualización incorrecto"
#
#     # Verificar que los cambios se aplicaron correctamente en la base de datos
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("SELECT rid, startdate, enddate FROM roomunavailable WHERE ruid = %s", (ruid,))
#         roomunavailable = cur.fetchone()
#         assert roomunavailable is not None, "La habitacion no se encontró después de actualizar"
#         assert roomunavailable[0] == updated_roomunavailable['rid'], "El id del hotel de la habitacion no se actualizó correctamente"
#         assert roomunavailable[1] == updated_roomunavailable['startdate'], "El id de la descripcion de la habitacion no se actualizó correctamente"
#         assert roomunavailable[2] == updated_roomunavailable['endddate'], "El precio de la habitacion no se actualizó correctamente"
#
#     finally:
#         cur.close()
#
#     # Eliminar la habitación de la base de datos
#     try:
#         cur = db.conexion.cursor()
#         cur.execute("DELETE FROM roomunavailable WHERE ruid = %s", (ruid,))
#         db.conexion.commit()
#     finally:
#         cur.close()
#         db.close()
#
# def test_post_room_with_missing_fields(client):
#     # Datos de la habitación con un dato faltante
#     new_roomunavailable_missing_field = {
#         "ruid": 1,
#         # "startdate": 10, Este campo se omite intencionalmente
#         "enddate": 100.50,
#     }
#
#     response = client.post('/roomunavailable', json=new_roomunavailable_missing_field)
#
#     # Verificar que la respuesta tenga un código de estado 400 (Bad Request)
#     assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"
#
#     response_data = response.get_json()
#     assert "error" in response_data, "Expected error message in the response"