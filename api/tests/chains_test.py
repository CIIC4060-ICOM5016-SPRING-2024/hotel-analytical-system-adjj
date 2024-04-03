from api.model.db import Database


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
    assert response_data['message'] == "Chain agregado exitosamente", "Expected success message in the response"

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
                DELETE FROM chain
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

if __name__=='__main__':
    
    test_post_chain()

