from api.model.db import Database

def test_get_reserve_by_id(client):
    for chid in range(1,6):
        response = client.get(f'/reserve/{chid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"
        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'ruid' in data, "'ruid' debe estar presente"
        assert 'clid' in data, "'clid' debe estar presente"
        assert 'total_cost' in data, "'total_cost' debe estar presente"
        assert 'payment' in data, "'payment' debe estar presente"
        assert 'guests' in data, "'guests' debe estar presente"
        assert isinstance(data['ruid'], int), "ruid debe ser un integer"
        assert isinstance(data['clid'], int), "clid debe ser un integer"
        assert isinstance(data['total_cost'], float), f"total_cost debe ser un float"
        assert isinstance(data['payment'], str), f"payment debe ser un string"
        assert isinstance(data['guests'], int), f"guests debe ser un integer"

def test_get_all_reserves(client):
    response = client.get('/reserve')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'reid' in data[i], "reid has to be a key"
            assert 'ruid' in data[i], "ruid has to be a key"
            assert 'clid' in data[i], "clid has to be a key"
            assert 'total_cost' in data[i], "total_cost has to be a key"
            assert 'payment' in data[i], "payment has to be a key"
            assert 'guests' in data[i], "guests has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['reid'], int)
            assert isinstance(data[i]['ruid'], int)
            assert isinstance(data[i]['clid'], int)
            assert isinstance(data[i]['total_cost'], float)
            assert isinstance(data[i]['payment'], str)
            assert isinstance(data[i]['guests'], int)
def test_post_reserve(client):
    new_reserve = {
        "ruid":4541,
        "clid":2,
        "total_cost": 32.45,
        "payment": 'cash',
        "guests":1,
        "eid": 9
}

    response = client.post('/reserve', json=new_reserve)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['message'] == "Reservation Added", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM reserve 
                    WHERE ruid = %s AND clid = %s AND total_cost = %s AND payment = %s AND guests = %s
                    """
        cur.execute(query, (new_reserve['ruid'], new_reserve['clid'], new_reserve['total_cost'], new_reserve['payment'], new_reserve['guests']))
        chain__ = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert chain__ is not None, "El reserve añadido no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el empleado a eliminar
        query = """
                DELETE FROM reserve
                WHERE  reid=%s AND ruid = %s AND clid = %s AND total_cost = %s AND payment = %s AND guests = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (new_reserve['reid'],new_reserve['ruid'], new_reserve['clid'], new_reserve['total_cost'], new_reserve['payment'], new_reserve['guests'])
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
def test_delete_reserve(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO reserve (ruid, clid, total_cost, payment, guests) VALUES (%s,%s,%s,%s,%s) RETURNING reid
        """,(4541,2,32.45,'cash',2))
        reid= cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro

        db.conexion.commit()
    except Exception as e:
        print(f"Error adding a reserve for DELETING test: {e}")
        db.conexion.rollback()    
        assert False, "Error adding a reserve for DELETING test"
    finally:
        cur.close()


    assert reid is not None, "Reserve was not added correctly"

    delete_response = client.delete(f'/reserve/{reid}')

    assert delete_response.status_code == 200, "Failed to eliminate chain"


    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM reserve WHERE reid = %s", (reid,))
        client__ = cur.fetchone()
        assert client__ is None, "El reserve no fue eliminado correctamente"
    finally:
        cur.close()
        db.close()


def test_put_reserve(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""INSERT INTO reserve (ruid, clid, total_cost, payment, guests) VALUES (%s,%s,%s,%s,%s) RETURNING reid""",(4541,2,32.45,'cash',2) )
        reid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    assert reid is not None, "Reserve was not added correctly"

    updated_reserve ={
        "ruid":4541,
        "clid":2,
        "total_cost": 32.45,
        "payment": 'credit card',
        "guests":2
    }

    updated_response = client.put(f'/reserve/{reid}',json=updated_reserve)
    assert updated_response.status_code == 200, "Failed to update client"

     # Verificar que los cambios se aplicaron correctamente
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT ruid, clid, total_cost, payment, guests FROM reserve WHERE reid = %s", (reid,))
        chain__ = cur.fetchone()
        assert chain__ is not None, "La reservacion no se encontró después de actualizar"
        assert chain__[0] == updated_reserve['ruid'], "El ruid del chain no se actualizó correctamente"
        assert chain__[1] == updated_reserve['clid'], "El clid del chain no se actualizó correctamente"
        assert chain__[2] == updated_reserve['total_cost'], "El total_cost del chain no se actualizó correctamente"
        assert chain__[3] == updated_reserve['payment'], "El payment del chain no se actualizó correctamente"
        assert chain__[4] == updated_reserve['guests'], "El guests del chain no se actualizó correctamente"
    finally:
        cur.close()

    # Eliminar el empleado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM reserve WHERE reid = %s", (reid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()


