

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