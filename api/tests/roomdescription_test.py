from api.model.db import Database

def test_get_all_room_descriptions(client):
    response = client.get('/roomdescription')
    assert response.status_code == 200, f"response code should be 200 but got {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "data should be a list"
    if data:  # Si hay datos, verifica la estructura de un elemento
        for i in range(len(data)):
            assert 'rdid' in data[i], "rdid has to be a key"
            assert 'rname' in data[i], "rname has to be a key"
            assert 'rtype' in data[i], "hname has to be a key"
            assert 'capacity' in data[i], "capacity has to be a key"
            assert 'ishandicap' in data[i], "ishandicap has to be a key"
            # Asegúrate de que los campos tienen los tipos de datos esperados
            assert isinstance(data[i]['rdid'], int), f"rdid has to be int but got {type(data[i]['rdid'])}"
            assert isinstance(data[i]['rname'], str), f"rname has to be str but got {type(data[i]['rname'])}"
            assert isinstance(data[i]['rtype'], str), f"rtype has to be str but got {type(data[i]['rtype'])}"
            assert isinstance(data[i]['capacity'], int), f"capacity has to be int but got {type(data[i]['capacity'])}"
            assert isinstance(data[i]['ishandicap'], bool), f"ishandicap has to be bool but got {type(data[i]['ishandicap'])}"

def test_get_room_descriptions_y_id(client):
    # Asumiendo que ya tienes un hotel en tu base de datos de prueba, utiliza ese ID. De lo contrario, inserta uno y obtén el ID.
    # Reemplaza esto con un ID válido de tu base de datos de prueba o después de insertar un hotel nuevo
    for rdid in range(1,62):
        response = client.get(f'/roomdescription/{rdid}')
        assert response.status_code == 200, f"El código de respuesta debe ser 200 pero se obtuvo {response.status_code}"

        data = response.get_json()
        assert isinstance(data, dict), "Los datos deben ser un diccionario"
        # Verifica que los datos del hotel tengan la estructura y tipos de datos esperados
        assert 'rdid' in data, "'rdid' debe estar presente"
        assert 'rname' in data, "'rname' debe estar presente"
        assert 'rtype' in data, "'rtype' debe estar presente"
        assert 'capacity' in data, "'capacity' debe estar presente"
        assert 'ishandicap' in data, "'ishandicap' debe estar presente"

        assert isinstance(data['rdid'], int), "rdid debe ser un entero"
        assert isinstance(data['rname'], str), "rname debe ser un str"
        assert isinstance(data['rtype'], str), "rtype debe ser un str"
        assert isinstance(data['capacity'], int), "capacity debe ser una int"
        assert isinstance(data['ishandicap'], bool), "ishandicap debe ser un bool"


def test_post_room_description(client):
    # Datos del nuevo empleado
    new_roomdescription = {
        "rname": "Standard",
        "rtype": "Basic",
        "capacity": 2,
        "ishandicap": True
    }

    # Enviar petición POST al endpoint /hotel con los datos del empleado
    response = client.post('/roomdescription', json=new_roomdescription)

    # Verificar que la respuesta tenga un código de estado 201 (creado)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    response_data = response.get_json()
    assert response_data['message'] == "Room description agregada exitosamente", "Expected success message in the response"

    db = Database()
    #Consulta directa con la base para ver asegurarnos de que si se añadio el elemento
    try:
        cur = db.conexion.cursor()
        query = """
                    SELECT * FROM roomdescription 
                    WHERE rname = %s AND rtype = %s AND capacity = %s AND ishandicap = %s
                    """
        cur.execute(query, (new_roomdescription['rname'], new_roomdescription['rtype'], new_roomdescription['capacity'], new_roomdescription['ishandicap']))
        roomdescription = cur.fetchone()  # Utiliza fetchone() para obtener el primer resultado que coincida
        assert roomdescription is not None, "El room description añadido no se encontró en la base de datos"
    finally:
        cur.close()

    #Consulta directa con la base para borrar el elemento añadido
    try:
        cur = db.conexion.cursor()
        # Construye la consulta DELETE utilizando todos los campos para especificar el hotel a eliminar
        query = """
                DELETE FROM roomdescription
                WHERE rname = %s AND rtype = %s AND capacity = %s AND ishandicap = %s
                """
        # Preparar los valores a utilizar en la consulta DELETE
        values = (
            new_roomdescription['rname'],
            new_roomdescription['rtype'],
            new_roomdescription['capacity'],
            new_roomdescription['ishandicap']

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