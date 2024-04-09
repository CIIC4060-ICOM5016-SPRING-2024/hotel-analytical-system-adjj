from api.model.db import Database

def test_get_top_paid_regular_employees_by_hotel(client):
    for hid in range(1,41):
        body = {
            "eid": 1
        }
        response = client.get(f'/hotel/{hid}/highestpaid', json=body)
        assert response.status_code == 200 or \
        response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel {hid}.",\
        f"El código de respuesta debe ser 200, pero se obtuvo {response.status_code}"

        data = response.get_json()
        if(isinstance(data, list)):
            assert isinstance(data, list), "Los datos deben ser una lista"
            assert len(data) <= 3, "La lista no debe contener más de 3 empleados"
            if data:
                for employee in data:
                    assert 'age' in employee, "'age' debe estar presente en cada empleado"
                    assert 'eid' in employee, "'eid' debe estar presente en cada empleado"
                    assert 'fname' in employee, "'fname' debe estar presente en cada empleado"
                    assert 'lname' in employee, "'lname' debe estar presente en cada empleado"
                    assert 'position' in employee and employee['position'] == 'Regular', "Todos los empleados deben ser 'Regular'"
                    assert 'salary' in employee, "'salary' debe estar presente en cada empleado"
                    assert 'hid' in employee and employee['hid'] == hid, f"'hid' debe ser {hid} en cada empleado"
                    # Verifica que los salarios estén en orden descendente
                    salaries = [emp['salary'] for emp in data]
                    assert salaries == sorted(salaries, reverse=True), "Los salarios deben estar en orden descendente"

    body = {
        "eid": 2#Regular
    }
    response = client.get(f'/hotel/{1}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 1"

    response = client.get(f'/hotel/{3}/highestpaid', json=body)
    assert response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel {3}.", \
        f"El empleado 2 no puede ver las estadisticas del hotel 1"

    response = client.get(f'/hotel/{9}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 1"

    response = client.get(f'/hotel/{10}/highestpaid', json=body)
    assert response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel 10.", \
        f"El empleado 2 no puede ver las estadisticas del hotel 10"

    body = {
        "eid": 3 #Administrator
    }
    response = client.get(f'/hotel/{10}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 10"
    response = client.get(f'/hotel/{1}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 1"
    response = client.get(f'/hotel/{2}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 2"
    response = client.get(f'/hotel/{20}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 20"
    body = {
        "eid": 4 #Supervisor
    }
    response = client.get(f'/hotel/{1}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado {body['eid']} no puede ver las estadisticas del hotel 1"
    response = client.get(f'/hotel/{2}/highestpaid', json=body)
    assert response.status_code == 200, f"El empleado {body['eid']} no puede ver las estadisticas del hotel 2"
    response = client.get(f'/hotel/{3}/highestpaid', json=body)
    assert response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel 3.", \
        f"El empleado {body['eid']} no puede ver las estadisticas del hotel 3"



def test_get_top5_credit_card_reservations_by_hotel(client):
    for hid in range(1, 41):  # Asumiendo que quieres probar para hoteles con ID del 1 al 40
        body = {
            "eid": 1
        }
        response = client.get(f'/hotel/{hid}/mostcreditcard', json=body)
        assert response.status_code == 200 or \
        response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel {hid}.",\
        f"El código de respuesta debe ser 200 para el hotel {hid}, pero se obtuvo {response.status_code}"

        data = response.get_json()
        if isinstance(data, list):
            assert isinstance(data, list), f"Los datos deben ser una lista para el hotel {hid}"
            assert len(data) <= 5, f"La lista no debe contener más de 5 clientes para el hotel {hid}"

            if data:
                for c in data:
                    assert 'clid' in c, f"'clid' debe estar presente en cada cliente para el hotel {hid}"
                    assert 'fname' in c, f"'fname' debe estar presente en cada cliente para el hotel {hid}"
                    assert 'lname' in c, f"'lname' debe estar presente en cada cliente para el hotel {hid}"
                    assert 'reservation_count' in c, f"'reservation_count' debe estar presente en cada cliente para el hotel {hid}"
                    assert isinstance(c['reservation_count'],
                                      int), f"'reservation_count' debe ser un entero para el cliente {c['clid']} en el hotel {hid}"

                    # Extraer los conteos de reservaciones de los clientes
                    reservation_counts = [c['reservation_count'] for c in data]
                    # Verificar que los conteos de reservaciones estén en orden descendente
                    assert reservation_counts == sorted(reservation_counts,reverse=True), "Los conteos de reservaciones deben estar en orden descendente para el hotel {hid}"

    body = {
        "eid": 2
    }
    response = client.get(f'/hotel/{1}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 1"

    response = client.get(f'/hotel/{3}/mostcreditcard', json=body)
    assert response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel {3}.", \
        f"El empleado 2 no puede ver las estadisticas del hotel 1"

    response = client.get(f'/hotel/{9}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 1"

    response = client.get(f'/hotel/{10}/mostcreditcard', json=body)
    assert response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel 10.", \
        f"El empleado 2 no puede ver las estadisticas del hotel 10"

    body = {
        "eid": 3
    }
    response = client.get(f'/hotel/{10}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 10"
    response = client.get(f'/hotel/{1}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 1"
    response = client.get(f'/hotel/{2}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 2"
    response = client.get(f'/hotel/{20}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado 2 no puede ver las estadisticas del hotel 20"
    body = {
        "eid": 4
    }
    response = client.get(f'/hotel/{1}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado {body['eid']} no puede ver las estadisticas del hotel 1"
    response = client.get(f'/hotel/{2}/mostcreditcard', json=body)
    assert response.status_code == 200, f"El empleado {body['eid']} no puede ver las estadisticas del hotel 2"
    response = client.get(f'/hotel/{3}/mostcreditcard', json=body)
    assert response.get_json() == f"El empleado {body['eid']} no tiene acceso a las estadísticas del hotel 3.",\
    f"El empleado {body['eid']} no puede ver las estadisticas del hotel 3"


def test_get_top3_least_reserve_rooms(client):
    # Empleado 9 tiene acceso al hotel 1
    employee_id = 9
    body = {"eid": employee_id}

    # Acceso al hotel 1
    response = client.get(f'/hotel/1/leastreserve', json=body)
    assert response.status_code == 200, "Employee 9 should have access to Hotel 1"

    # Acceso en los demás hoteles
    for hid in range(2, 41):
        response = client.get(f'/hotel/{hid}/leastreserve', json=body)
        expected_status_code = 200
        assert response.status_code == expected_status_code, f"Employee 9 should not have access to Hotel {hid}, expected {expected_status_code}, got {response.status_code}"



def test_get_top_5_handicap_reserved(client):
    # Empleado 9 tiene acceso al hotel 1
    employee_id = 9
    body = {"eid": employee_id}

    # Acceso al hotel 1
    response = client.get(f'/hotel/1/handicaproom', json=body)
    assert response.status_code == 200, "Employee 9 should have access to Hotel 1"

    # Acceso en los demás hoteles
    for hid in range(2, 41):
        response = client.get(f'/hotel/{hid}/handicaproom', json=body)
        expected_status_code = 200
        assert response.status_code == expected_status_code, f"Employee 9 should not have access to Hotel {hid}, expected {expected_status_code}, got {response.status_code}"

def test_get_total_reservations_by_room_type(client):
    employee_id = 9
    body = {"eid": employee_id}

    # Acceso al hotel 1
    response = client.get(f'/hotel/1/totalreservations', json=body)
    assert response.status_code == 200, "Employee 9 should have access to Hotel 1"

     # Acceso en los demás hoteles
    for hid in range(2, 41):
        response = client.get(f'/hotel/{hid}/totalreservations', json=body)
        expected_status_code = 200
        assert response.status_code == expected_status_code, f"Employee 9 should not have access to Hotel {hid}, expected {expected_status_code}, got {response.status_code}"
