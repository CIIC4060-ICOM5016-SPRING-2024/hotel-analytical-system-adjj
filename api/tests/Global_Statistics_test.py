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
            "hid": 28,
            "hname": "Wolf-Deckow",
            "reservation_count": 174
          },
          {
            "hid": 1,
            "hname": "Goodwin, Kohler and Bechtelar",
            "reservation_count": 173
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

    # Verificar si el hotel con hid=28 tiene el mayor número de reservaciones
    response1 = client.get('/most/reservation')
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1[0]['hid'] == 28

    # Añadir reservaciones al hotel con hid=30
    add_reservations(hotel_id=30, num_reservations=34)

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
    assert data3[0]['hid'] == 28

    # Eliminar las reservaciones añadidas para restaurar el estado inicial
    remove_reservations(hotel_id=30, num_reservations=32)
