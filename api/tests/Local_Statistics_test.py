

def test_get_top_paid_regular_employees_by_hotel(client):
    for hid in range(1,41):
        response = client.get(f'/hotel/{hid}/highestpaid')
        assert response.status_code == 200, f"El código de respuesta debe ser 200, pero se obtuvo {response.status_code}"

        data = response.get_json()
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


def test_get_top5_credit_card_reservations_by_hotel(client):
    for hid in range(1, 41):  # Asumiendo que quieres probar para hoteles con ID del 1 al 40
        response = client.get(f'/hotel/{hid}/mostcreditcard')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 para el hotel {hid}, pero se obtuvo {response.status_code}"

        data = response.get_json()
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