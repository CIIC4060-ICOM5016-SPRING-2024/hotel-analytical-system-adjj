from api.model.db import Database

def test_get_most_reservations(client):
    def add_reservations(hotel_id, num_reservations):
        """Añade un número específico de reservaciones a un hotel."""
        db = Database()
        cur = db.conexion.cursor()
        for _ in range(num_reservations):
            cur.execute("""
                INSERT INTO Reserve (ruid, clid, total_cost, payment, guests)
                VALUES ((SELECT ruid FROM RoomUnavailable WHERE rid IN (SELECT rid FROM Room WHERE hid=%s) LIMIT 1),
                        (SELECT clid FROM Client LIMIT 1),
                        100.00, 'Credit Card', 2)
            """, (hotel_id,))
        db.conexion.commit()
        cur.close()
        db.close()

    def remove_reservations(hotel_id, num_reservations):
        """Elimina un número específico de reservaciones de un hotel. Mas espesifico los ultimos que fueron añdidos."""
        db = Database()
        cur = db.conexion.cursor()
        cur.execute("""
            DELETE FROM Reserve
            WHERE reid IN (
                SELECT re.reid FROM Reserve re
                JOIN RoomUnavailable ru ON re.ruid = ru.ruid
                JOIN Room r ON ru.rid = r.rid
                WHERE r.hid = %s
                ORDER BY re.reid DESC
                LIMIT %s
            )
        """, (hotel_id, num_reservations))
        db.conexion.commit()
        cur.close()
        db.close()

    """Suponiendo que esta es la respuesta inicial correcta:
        [
          {
            "hid": 1,
            "hname": "Goodwin, Kohler and Bechtelar",
            "reservation_count": 173
          },
          {
            "hid": 28,
            "hname": "Wolf-Deckow",
            "reservation_count": 164
          },
          {
            "hid": 30,
            "hname": "O'Reilly, Hermiston and Dickens",
            "reservation_count": 141
          },
          {
            "hid": 32,
            "hname": "Barton, Hyatt and Daugherty",
            "reservation_count": 140
          }
        ]"""

    # Verificar si el hotel con hid=1 tiene el mayor número de reservaciones
    response1 = client.get('/most/reservation')
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1[0]['hid'] == 1

    # Añadir reservaciones al hotel con hid=30
    add_reservations(hotel_id=30, num_reservations=33)

    # Verificar si el hotel con hid=30 ahora tiene el mayor número de reservaciones
    response2 = client.get('/most/reservation')
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2[0]['hid'] == 30

    remove_reservations(hotel_id=30, num_reservations=2)

    # Verificar si el hotel con hid=28 vuelve a tener el mayor número de reservaciones
    response3 = client.get('/most/reservation')
    assert response3.status_code == 200
    data3 = response3.get_json()
    assert data3[0]['hid'] == 1

    # Eliminar las reservaciones añadidas para restaurar el estado inicial
    remove_reservations(hotel_id=30, num_reservations=31)




def test_get_hotels_with_most_capacity(client):
    # No es necesario modificar los datos antes del primer chequeo porque ya tienes el estado inicial esperado

    # Verificar si la respuesta inicial es correcta
    initial_response = client.get('/most/capacity')
    assert initial_response.status_code == 200
    initial_data = initial_response.get_json()
    expected_initial_response = [
        {"hid": 1, "hname": "Goodwin, Kohler and Bechtelar", "total_capacity": 76},
        {"hid": 28, "hname": "Wolf-Deckow", "total_capacity": 73},
        {"hid": 5, "hname": "Bartoletti-Stanton", "total_capacity": 69},
        {"hid": 40, "hname": "Fadel, Cummerata and Littel", "total_capacity": 66},
        {"hid": 17, "hname": "Rodriguez-Casper", "total_capacity": 65}
    ]
    assert initial_data == expected_initial_response

    # Función para añadir/modificar la capacidad de habitaciones en un hotel específico
    def adjust_hotel_capacity(hotel_id, additional_capacity,num_rooms):
        """Añade habitaciones a un hotel para incrementar su capacidad total.

            Args:
                db (Database): Instancia de la base de datos.
                hotel_id (int): El ID del hotel a ajustar.
                additional_capacity (int): La capacidad adicional por habitación.
                num_rooms (int): Número de habitaciones a añadir.
            """
        db = Database()
        cur = db.conexion.cursor()
        # Crear una nueva descripción de habitación con la capacidad deseada
        cur.execute("""
                INSERT INTO RoomDescription (rname, rtype, capacity, ishandicap)
                VALUES (%s, %s, %s, %s) RETURNING rdid;
            """, ('Standard Plus', 'Double', additional_capacity, False))
        rdid = cur.fetchone()[0]

        # Añadir las habitaciones al hotel
        for _ in range(num_rooms):
            cur.execute("""
                    INSERT INTO Room (hid, rdid, rprice)
                    VALUES (%s, %s, 100.00);
                """, (hotel_id, rdid))

        db.conexion.commit()
        cur.close()
        db.close()

    # Función para revertir los cambios hechos por adjust_hotel_capacity
    def revert_hotel_capacity_adjustments(hotel_id, additional_capacity, num_rooms):
        """Revierte los ajustes de capacidad hechos a un hotel.

            Args:
                db (Database): Instancia de la base de datos.
                hotel_id (int): El ID del hotel a ajustar.
                additional_capacity (int): La capacidad que se había añadido por habitación.
                num_rooms (int): Número de habitaciones que se habían añadido.
            """
        db = Database()
        cur = db.conexion.cursor()
        # Identificar la descripción de habitación usada para el ajuste
        cur.execute("""
                SELECT rdid FROM RoomDescription
                WHERE capacity = %s
                ORDER BY rdid DESC LIMIT 1;
            """, (additional_capacity,))
        rdid = cur.fetchone()[0]

        # Eliminar las últimas habitaciones añadidas que usen esa descripción
        cur.execute("""
                DELETE FROM Room
                WHERE rid IN (
                    SELECT rid FROM Room
                    WHERE hid = %s AND rdid = %s
                    ORDER BY rid DESC
                    LIMIT %s
            );
            """, (hotel_id, rdid, num_rooms))

        # Ahora, eliminar la descripción de habitación 'dummy' creada para el ajuste
        cur.execute("""
                    DELETE FROM RoomDescription
                    WHERE rdid = %s;
                """, (rdid,))

        db.conexion.commit()
        cur.close()
        db.close()

    # Ajustar la capacidad de un hotel para cambiar su ranking (en este caso, aumentando la capacidad del hotel con hid=28)
    adjust_hotel_capacity(hotel_id=28, additional_capacity=1, num_rooms=4)

    # Verificar si el cambio se refleja correctamente
    updated_response = client.get('/most/capacity')
    assert updated_response.status_code == 200
    updated_data = updated_response.get_json()
    # Asumiendo que el cambio hecho debería colocar al hotel con hid=28 en la cima
    assert updated_data[0]['hid'] == 28

    # Revertir los cambios para restaurar el estado inicial
    revert_hotel_capacity_adjustments(hotel_id=28, additional_capacity=1, num_rooms=4)

    # (Opcional) Verificar que el estado se haya restaurado efectivamente podría ser parte de otra prueba




def test_get_highest_revenue_chains(client):
    # Scenario 1: Employee without access to global statistics
    employee_id = 9  # Assuming employee with ID 9 doesn't have access
    body = {"eid": employee_id}
    response = client.get('/most/revenue', json=body)  # Adjust endpoint as needed
    if response.status_code != 200:
        assert response.get_json() == {"error": f"El empleado {employee_id} no tiene acceso a las estadísticas globales."}, "Expected access error message"



    employee_id_with_access = 3  # Assuming employee with ID 3 has access
    body = {"eid": employee_id_with_access}
    response = client.get('/least/rooms', json=body)  # Adjust endpoint as needed
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    # Expected results in the specified format
    expected_results = [
        {"chain_id": 5, "chain_name": "Ferry Torp's Logs", "total_revenue": 1548260.0899999996},
        {"chain_id": 1, "chain_name": "Bergaum-Champlin", "total_revenue": 1531435.7200000002},
        {"chain_id": 4, "chain_name": "Howe-Caroll", "total_revenue": 1302918.3899999994}
    ]
    response = client.get('/most/revenue', json=body)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.get_json()
    # Validate the length of the response to ensure only 3 results are returned
    # assert len(data) == 3, f"Expected 3 results, but got {len(data)}"

    # Validate each item in the response against the expected results
    for expected in expected_results:
        # Find a matching item in response data
        match = next((item for item in data if item["chain_id"] == expected["chain_id"]), None)
        assert match is not None, f"Expected result for chain_id {expected['chain_id']} not found in response."
        assert match["chain_name"] == expected["chain_name"], f"Expected chain_name for chain_id {expected['chain_id']} to be {expected['chain_name']}, got {match['chain_name']}"
        assert abs(match["total_revenue"] - expected["total_revenue"]) < 0.01, f"Expected total_revenue for chain_id {expected['chain_id']} to be {expected['total_revenue']}, got {match['total_revenue']}"


def test_top_3_chains_with_least_rooms(client):
    # Scenario 1: Employee without global stats access
    employee_id = 9  # Assuming employee with ID 9 doesn't have access
    body = {"eid": employee_id}
    response = client.get('/least/rooms', json=body)  # Adjust endpoint as needed
    if response.status_code != 200:
        assert response.get_json() == {"error": f"El empleado {employee_id} no tiene acceso a las estadísticas globales."}, "Expected access error message"

    # Scenario 2: Employee with global stats access
    employee_id = 3  # Assuming employee with ID 3 has access
    body = {"eid": employee_id}
    response = client.get('/least/rooms', json=body)  # Adjust endpoint as needed
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    expected_results = [
        {
            "chain_id": -1,
            "chain_name": "Administrative ",
            "room_count": 0
        },
        {
            "chain_id": 3,
            "chain_name": "Murphy and Boyles",
            "room_count": 72
        },
        {
            "chain_id": 2,
            "chain_name": "Wisozk Inc.",
            "room_count": 81
        }
    ]

    data = response.get_json()
    # Assuming the response data is a list of dictionaries matching expected_results
    for expected in expected_results:
        # Find a matching item in response data
        match = next((item for item in data if item["chain_id"] == expected["chain_id"]), None)
        assert match is not None, f"Expected result for chain_id {expected['chain_id']} not found in response."
        assert match["room_count"] == expected["room_count"], f"Expected room_count for chain_id {expected['chain_id']} to be {expected['room_count']}, got {match['room_count']}"


