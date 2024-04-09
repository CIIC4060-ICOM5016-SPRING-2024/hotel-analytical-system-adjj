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
    def add_revenue(chain_id, amount):
        """Adds a specific revenue amount to a chain by creating a reservation."""
        db = Database()
        cur = db.conexion.cursor()
        # Find a hotel in the specified chain
        cur.execute("SELECT hid FROM Hotel WHERE chid=%s LIMIT 1", (chain_id,))
        hotel_id = cur.fetchone()[0]
        # Find a room in the specified hotel
        cur.execute("SELECT rid FROM Room WHERE hid=%s LIMIT 1", (hotel_id,))
        room_id = cur.fetchone()[0]
        # Find an unavailable room instance
        cur.execute("SELECT ruid FROM RoomUnavailable WHERE rid=%s LIMIT 1", (room_id,))
        room_unavailable_id = cur.fetchone()[0]
        # Find a client
        cur.execute("SELECT clid FROM Client LIMIT 1")
        client_id = cur.fetchone()[0]
        # Insert a reservation with specified revenue
        cur.execute("""
            INSERT INTO Reserve (ruid, clid, total_cost, payment, guests)
            VALUES (%s, %s, %s, 'Credit Card', 2)
        """, (room_unavailable_id, client_id, amount))
        db.conexion.commit()
        cur.close()
        db.close()

    def remove_revenue(chain_id, amount):
        """Removes a specific revenue amount from a chain by deleting a reservation."""
        db = Database()
        cur = db.conexion.cursor()
        cur.execute("""
            DELETE FROM Reserve
            WHERE reid IN (
                SELECT re.reid FROM Reserve re
                JOIN RoomUnavailable ru ON re.ruid = ru.ruid
                JOIN Room r ON ru.rid = r.rid
                JOIN Hotel h ON r.hid = h.hid
                WHERE h.chid = %s AND re.total_cost = %s
                ORDER BY re.reid DESC LIMIT 1
            )
        """, (chain_id, amount))
        db.conexion.commit()
        cur.close()
        db.close()

    # Check the initial state to confirm "Ferry Torp's Logs" has the highest revenue
    response1 = client.get('/most/revenue')
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1[0]['chain_id'] == 5  # Assuming the first item in the list is the highest

    # Add revenue to "Howe-Caroll" (chain_id=4)
    add_revenue(chain_id=4, amount=300000)  # This amount should be enough to make it the top

    # Check if "Howe-Caroll" now has the highest revenue
    response2 = client.get('/most/revenue')
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2[0]['chain_id'] == 4

    # Remove the added revenue to restore the initial state
    remove_revenue(chain_id=4, amount=300000)

    # Re-verify the initial state
    response3 = client.get('/most/revenue')
    assert response3.status_code == 200
    data3 = response3.get_json()
    assert data3[0]['chain_id'] == 5



# def test_get_top_3_chains_with_least_rooms(client):
#     def add_rooms(chain_id, num_rooms):
#         """Adds a specific number of rooms to the first hotel found in the specified chain."""
#         db = Database()
#         cur = db.conexion.cursor()
#         # Find the first hotel in the specified chain
#         cur.execute("SELECT hid FROM Hotel WHERE chid=%s LIMIT 1", (chain_id,))
#         hotel_id = cur.fetchone()[0]
#         # Assuming there's at least one RoomDescription to use, add rooms to the hotel
#         for _ in range(num_rooms):
#             cur.execute("""
#                 INSERT INTO Room (hid, rdid, rprice)
#                 VALUES (%s, (SELECT rdid FROM RoomDescription LIMIT 1), 100.00)
#             """, (hotel_id,))
#         db.conexion.commit()
#         cur.close()
#         db.close()
#
#     def remove_rooms(chain_id, num_rooms):
#         """Removes a specific number of the most recently added rooms from the first hotel found in the specified chain."""
#         db = Database()
#         cur = db.conexion.cursor()
#         # Find the first hotel in the specified chain
#         cur.execute("SELECT hid FROM Hotel WHERE chid=%s LIMIT 1", (chain_id,))
#         hotel_id = cur.fetchone()[0]
#         # Remove the specified number of most recently added rooms from the hotel
#         cur.execute("""
#             DELETE FROM Room
#             WHERE rid IN (
#                 SELECT rid FROM Room
#                 WHERE hid = %s
#                 ORDER BY rid DESC
#                 LIMIT %s
#             )
#         """, (hotel_id, num_rooms))
#         db.conexion.commit()
#         cur.close()
#         db.close()
#
#     # Verify the initial state matches the expected output
#     response1 = client.get('/least/rooms')
#     assert response1.status_code == 200
#     data1 = response1.get_json()
#     assert data1[0]['chain_name'] == "Administrative " and data1[0]['room_count'] == 0
#
#     # Add rooms to "Murphy and Boyles" chain to change its ranking
#     add_rooms(chain_id=3, num_rooms=20)
#
#     # Verify "Murphy and Boyles" is no longer in the top 3 chains with the least number of rooms
#     response2 = client.get('/least/rooms')
#     assert response2.status_code == 200
#     data2 = response2.get_json()
#     assert all(chain['chain_id'] != 3 for chain in data2)
#
#     # Remove the added rooms to restore the initial state
#     remove_rooms(chain_id=3, num_rooms=20)
#
#     # Re-verify the initial state to ensure the changes have been reverted
#     response3 = client.get('/least/rooms')
#     assert response3.status_code == 200
#     data3 = response3.get_json()
#     assert data3[1]['chain_name'] == "Murphy and Boyles" and data3[1]['room_count'] == 72

def test_get_top_3_chains_with_least_rooms(client):
    # Assuming eid 1 has access to global statistics
    access_eid = 3

    def add_rooms(chain_id, num_rooms):
        """Adds a specific number of rooms to the first hotel found in the specified chain."""
        db = Database()
        cur = db.conexion.cursor()
        # Find the first hotel in the specified chain
        cur.execute("SELECT hid FROM Hotel WHERE chid=%s LIMIT 1", (chain_id,))
        hotel_id = cur.fetchone()[0]
        # Assuming there's at least one RoomDescription to use, add rooms to the hotel
        for _ in range(num_rooms):
            cur.execute("""
                INSERT INTO Room (hid, rdid, rprice)
                VALUES (%s, (SELECT rdid FROM RoomDescription LIMIT 1), 100.00)
            """, (hotel_id,))
        db.conexion.commit()
        cur.close()
        db.close()

    def remove_rooms(chain_id, num_rooms):
        """Removes a specific number of the most recently added rooms from the first hotel found in the specified chain."""
        db = Database()
        cur = db.conexion.cursor()
        # Find the first hotel in the specified chain
        cur.execute("SELECT hid FROM Hotel WHERE chid=%s LIMIT 1", (chain_id,))
        hotel_id = cur.fetchone()[0]
        # Remove the specified number of most recently added rooms from the hotel
        cur.execute("""
            DELETE FROM Room 
            WHERE rid IN (
                SELECT rid FROM Room 
                WHERE hid = %s
                ORDER BY rid DESC
                LIMIT %s
            )
        """, (hotel_id, num_rooms))
        db.conexion.commit()
        cur.close()
        db.close()

    # Verify the initial state matches the expected output
    response1 = client.post('/least/rooms', json={'eid': access_eid})
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1[0]['chain_name'] == "Administrative" and data1[0]['room_count'] == 0

    # Add rooms to "Murphy and Boyles" chain to change its ranking
    add_rooms(chain_id=3, num_rooms=20)

    # Verify "Murphy and Boyles" is no longer in the top 3 chains with the least number of rooms
    response2 = client.post('/least/rooms', json={'eid': access_eid})
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert all(chain['chain_id'] != 3 for chain in data2)

    # Remove the added rooms to restore the initial state
    remove_rooms(chain_id=3, num_rooms=20)

    # Re-verify the initial state to ensure the changes have been reverted
    response3 = client.post('/least/rooms', json={'eid': access_eid})
    assert response3.status_code == 200
    data3 = response3.get_json()
    assert data3[1]['chain_name'] == "Murphy and Boyles" and data3[1]['room_count'] == 72



