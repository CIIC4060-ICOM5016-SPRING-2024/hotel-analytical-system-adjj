from api.model.db import Database

def test_get_chain_by_id(client):
    for chid in range(1,6):
        response = client.get(f'/chains/{chid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"
        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'cname' in data, "'chid' debe estar presente"
        assert 'springmkup' in data, "cname' debe estar presente"
        assert 'summermkup' in data, "'springmkup' debe estar presente"
        assert 'fallmkup' in data, "'summermkup' debe estar presente"
        assert 'wintermkup' in data, "'fallmkup' debe estar presente"
        assert isinstance(data['cname'], str), "cname debe ser un string"
        assert isinstance(data['springmkup'], float), "springmkup debe ser un float"
        assert isinstance(data['summermkup'], float), f"summermkup debe ser un float"
        assert isinstance(data['fallmkup'], float), f"fallmkup debe ser un float"
        assert isinstance(data['wintermkup'], float), f"wintermkup debe ser un float"

def test_get_all_chains(client):
    response = client.get('/chains')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'chid' in data[i], "chid has to be a key"
            assert 'cname' in data[i], "cname has to be a key"
            assert 'springmkup' in data[i], "springmkup has to be a key"
            assert 'summermkup' in data[i], "summermkup has to be a key"
            assert 'fallmkup' in data[i], "fallmkup has to be a key"
            assert 'wintermkup' in data[i], "wintermkup has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['chid'], int)
            assert isinstance(data[i]['cname'], str)
            assert isinstance(data[i]['springmkup'], float)
            assert isinstance(data[i]['summermkup'], float)
            assert isinstance(data[i]['fallmkup'], float)
            assert isinstance(data[i]['wintermkup'], float)
def test_post_chain(client):
    # Datos del nuevo empleado
    new_chain = {
    "chid":10,
    "cname":"Gato Blanco",
    "springmkup":2,
    "summermkup":2,
    "fallmkup":2,
    "wintermkup":2
}

    # Enviar petición POST al endpoint /employee con los datos del empleado
    response = client.post('/chains', json=new_chain)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['message'] == "Chain added", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM chains 
                    WHERE cname = %s AND springmkup = %s AND summermkup = %s AND fallmkup = %s AND wintermkup = %s
                    """
        cur.execute(query, (new_chain['cname'], new_chain['springmkup'], new_chain['summermkup'], new_chain['fallmkup'], new_chain['wintermkup']))
        chain__ = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert chain__ is not None, "El chain añadido no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el empleado a eliminar
        query = """
                DELETE FROM chains
                WHERE cname = %s AND springmkup = %s AND summermkup = %s AND fallmkup = %s AND wintermkup = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (new_chain['cname'], new_chain['springmkup'], new_chain['summermkup'], new_chain['fallmkup'], new_chain['wintermkup'])
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
def test_delete_chain(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""
            INSERT INTO chains (cname, springmkup, summermkup, fallmkup, wintermkup) VALUES (%s,%s,%s,%s,%s) RETURNING chid
        """,("Gato Blanco",2,2,2,2))
        chid = cur.fetchone()[0]  # Asume que INSERT...RETURNING retorna el eid del nuevo registro

        db.conexion.commit()
    except Exception as e:
        print(f"Error adding a chain for DELETING test: {e}")
        db.conexion.rollback()    
        assert False, "Error adding a chain for DELETING test"
    finally:
        cur.close()


    assert chid is not None, "Chain was not added correctly"

    delete_response = client.delete(f'/chains/{chid}')

    assert delete_response.status_code == 200, "Failed to eliminate chain"


    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT * FROM chains WHERE chid = %s", (chid,))
        client__ = cur.fetchone()
        assert client__ is None, "El client no fue eliminado correctamente"
    finally:
        cur.close()
        db.close()


def test_put_chain(client):
    db = Database()
    try:
        cur = db.conexion.cursor()
        cur.execute("""INSERT INTO chains (cname, springmkup, summermkup, fallmkup, wintermkup) VALUES (%s,%s,%s,%s,%s) RETURNING chid""", ("Gato Blanco",3,3,3,3))
        chid = cur.fetchone()[0]
        db.conexion.commit()
    finally:
        cur.close()

    assert chid is not None, "Chain was not added correctly"

    updated_chain ={
        "cname":"Gato Azul",
        "springmkup":2,
        "summermkup":2,
        "fallmkup":2,
        "wintermkup":2
    }

    updated_response = client.put(f'/chains/{chid}',json=updated_chain)
    assert updated_response.status_code == 200, "Failed to update client"

     # Verificar que los cambios se aplicaron correctamente
    try:
        cur = db.conexion.cursor()
        cur.execute("SELECT cname, springmkup, summermkup, fallmkup, wintermkup FROM chains WHERE chid = %s", (chid,))
        chain__ = cur.fetchone()
        assert chain__ is not None, "El empleado no se encontró después de actualizar"
        assert chain__[0] == updated_chain['cname'], "El cname del chain no se actualizó correctamente"
        assert chain__[1] == updated_chain['springmkup'], "El springmkup del chain no se actualizó correctamente"
        assert chain__[2] == updated_chain['summermkup'], "El summermkup del chain no se actualizó correctamente"
        assert chain__[3] == updated_chain['fallmkup'], "El fallmkup del chain no se actualizó correctamente"
        assert chain__[4] == updated_chain['wintermkup'], "El wintermkup del chain no se actualizó correctamente"
    finally:
        cur.close()

    # Eliminar el empleado de la base de datos
    try:
        cur = db.conexion.cursor()
        cur.execute("DELETE FROM chains WHERE chid = %s", (chid,))
        db.conexion.commit()
    finally:
        cur.close()
        db.close()


