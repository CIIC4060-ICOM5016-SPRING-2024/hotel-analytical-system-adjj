import pandas as pd
import sqlite3
import os
from api.model.db import Database
import io
from psycopg2 import sql

DATA_PATH = os.path.abspath(os.path.join(os.getcwd(), "..", "Phase#1_data"))
CLEAN_DATA_DIR = os.path.join(DATA_PATH, "cleanData")
NAME_FILES = [file for file in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, file))]


column_mappings = {
    'chain.xlsx': {
        'id': 'chid',
        'name': 'cname',
        'spring': 'springmkup',
        'summer': 'summermkup',
        'fall': 'fallmkup',
        'winter': 'wintermkup'
    },
    'client.csv': {
        'clid': 'clid',
        'fname': 'fname',
        'lastname': 'lname',
        'age': 'age',
        'memberyear': 'memberyear'
    },
    'employee.json': {
        'employeeid': 'eid',
        'hotelid': 'hid',
        'firstname': 'fname',
        'lastname': 'lname',
        'age': 'age',
        'salary': 'salary',
        'position': 'position'
    },
    'hotel.csv': {
        'hid': 'hid',
        'chain': 'chid',
        'name': 'hname',
        'city': 'hcity'
    },
    'login.xlsx': {
        'lid': 'lid',
        'employeeid': 'eid',
        'user': 'username',
        'pass': 'password'
    },
    'reservations.db': {
        'reid': 'reid',
        'ruid': 'ruid',
        'clid': 'clid',
        'total_cost': 'total_cost',
        'payment': 'payment',
        'guests': 'guests'
    },
    'roomdetails.json': {
        'detailid': 'rdid',
        'name': 'rname',
        'type': 'rtype',
        'capacity': 'capacity',
        'handicap': 'ishandicap'
    },
    'rooms.db': {
        'rid': 'rid',
        'hid': 'hid',
        'rdid': 'rdid',
        'rprice': 'rprice'
    },
    'room_unavailable.csv': {
        'ruid': 'ruid',
        'rid': 'rid',
        'start_date': 'startdate',
        'end_date': 'enddate'
    }
}



def make_data_frame(file_path:str) -> pd.DataFrame:
    """
        Lee un archivo de datos de una ruta especificada y carga los datos en un DataFrame de pandas.

        Argumentos:
        file_path (str): La ruta completa al archivo de datos. El archivo puede ser de tipo .csv, .xlsx, .json o .db.

        Devuelve:
        pd.DataFrame: Un DataFrame de pandas que contiene los datos cargados del archivo especificado.

        Lanza:
        ValueError: Si la extensión del archivo no es soportada (.csv, .xlsx, .json, .db).
        Exception: Si no se encuentra una tabla adecuada en un archivo .db.
        """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, index_col=None)

    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, index_col=None)

    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)

    elif file_path.endswith('.db'):
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Obtiene una lista de todas las tablas en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Filtra las tablas que no quieres incluir
        tables = [table[0] for table in tables if table[0] not in ('sqlite_sequence', 'sqlite_master')]

        if tables:
            # Asume que hay exactamente una tabla de interés
            table_name = tables[0]
            print(f"\nUsing table: {table_name}\n")

            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        else:
            raise Exception("No suitable table found in the database.")

        conn.close()

    else:
        raise ValueError(f"Unsupported file extension for file: {file_path}")

    return df


def clean_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
        Limpia un DataFrame de pandas eliminando filas completamente vacías y filas que contengan
        al menos un campo vacío o nulo en cualquier columna.

        Argumentos:
        df (pd.DataFrame): El DataFrame de pandas que será limpiado.

        Devuelve:
        pd.DataFrame: Un DataFrame de pandas limpio sin filas completamente vacías ni filas con campos vacíos o nulos.
        """
    clean_df = df.dropna(how='all')
    header = clean_df.columns.tolist()

    for h in header:
        condition = clean_df[h].isnull() | (clean_df[h] == '')
        clean_df = clean_df[~condition]

    return clean_df


def write_clean_data_to_file(target_directory: str, file_name: str, df: pd.DataFrame) -> None:
    """
        Escribe un DataFrame de pandas en un archivo en el directorio objetivo. El formato del archivo de salida se determina por la extensión del nombre del archivo.

        Argumentos:
        target_directory (str): La ruta al directorio donde el archivo será escrito.

        file_name (str): El nombre del archivo, incluyendo la extensión, que determina el formato del archivo de salida.

        df (pd.DataFrame): El DataFrame de pandas que será escrito en el archivo.

        Devuelve:
        None

        Notas:
        - Los archivos .csv, .xlsx, y .json son directamente soportados mediante las funciones to_csv, to_excel, y to_json de pandas.
        - Para archivos .db, se asume una única tabla de interés y el nombre de la tabla va a ser igual al del archivo.
        - Si la extensión del archivo no es soportada, se imprimirá un mensaje y la función no realizará ninguna acción.
        """
    # Construye la ruta completa de destino usando el nombre del archivo y el directorio objetivo
    file_name_without_extension = file_name.split(".")[0]
    target_path = os.path.join(target_directory, file_name)

    if file_name.endswith('.csv'):
        df.to_csv(target_path, index=False)
    elif file_name.endswith('.xlsx'):
        df.to_excel(target_path, index=False)
    elif file_name.endswith('.json'):
        df.to_json(target_path, orient='records', lines=True)
    elif file_name.endswith('.db'):
        # Asumiendo que conoces el nombre de la tabla o lo tienes almacenado en alguna parte
        table_name = file_name_without_extension
        conn = sqlite3.connect(target_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
    else:
        print(f"Skipping unsupported file format for file: {file_name}")


def apply_column_mappings(df_list):
    for idx, (file_name, df) in enumerate(df_list):
        file_key = os.path.basename(file_name)
        if file_key in column_mappings:
            mapping = {k: v.strip() for k, v in column_mappings[file_key].items()}  # Ajuste aquí
            df.rename(columns=mapping, inplace=True)
            df_list[idx] = (file_name, df)  # Actualizar el DataFrame en df_list
            print(f'Columnas mapeadas para {file_name}: {df.columns.tolist()}')
        else:
            print(f'No se encontró mapeo para {file_name}')


def fix_datatype_columns(df_list):
    for file_name, df in df_list:
        # Verificar si el DataFrame actual es 'roomdetails.json' por su nombre de archivo
        if 'roomdetails.json' in file_name:
            # Convertir la columna 'ishandicap' de enteros a booleanos
            df['ishandicap'] = df['ishandicap'].astype(bool)

        if 'chain.xlsx' in file_name:
            # Convertir la columna 'ishandicap' de enteros a booleanos
            df['chid'] = df['chid'].astype(int)

        if 'client.csv' in file_name:
            # Convertir la columna 'ishandicap' de enteros a booleanos
            # print(df.dtypes)
            df['clid'] = df['clid'].astype(int)
            df['age'] = df['age'].astype(int)
            df['memberyear'] = df['memberyear'].astype(int)
            # print(df.dtypes)
            # print(df)


def insert_df_to_table(df, table_name):
    """
    Inserta un DataFrame en una tabla específica en la base de datos.
    """
    # Crea un buffer de memoria similar a un archivo
    buffer = io.StringIO()
    db = Database()
    # Escribe el DataFrame al buffer en formato CSV, sin el índice
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)  # Regresa al inicio del buffer para leer desde él

    cols = ','.join(list(df.columns))
    sql_query = sql.SQL("COPY {} ({}) FROM STDIN WITH CSV").format(sql.Identifier(table_name), sql.SQL(cols))

    try:
        cursor = db.conexion.cursor()
        cursor.copy_expert(sql_query, buffer)
        db.conexion.commit()
        cursor.close()
        print(f"Datos insertados correctamente en la tabla {table_name}.")
    except Exception as e:
        print(f"Error al insertar datos en la tabla {table_name}: {e}")
        db.conexion.rollback()


def insert_in_tables(df_list):
    """
    Inserta cada DataFrame en la tabla correspondiente siguiendo el orden de dependencias de las claves foráneas.
    """
    # Asignación de DataFrames a tablas basada en alguna lógica o mapeo predefinido
    # Por ejemplo, supongamos que los nombres de los archivos están mapeados a nombres de tablas

    table_mapping = {
        'chain.xlsx': 'chains',
        'hotel.csv': 'hotel',
        'employee.json': 'employee',
        'roomdetails.json': 'roomdescription',
        'rooms.db': 'room',
        'room_unavailable.csv': 'roomunavailable',
        'client.csv': 'client',
        'reservations.db': 'reserve',
        'login.xlsx': 'login',
    }

    # Orden basado en las dependencias de claves foráneas
    insert_order = ['chains', 'hotel', 'employee', 'roomdescription', 'room', 'roomunavailable', 'client', 'reserve',
                    'login']

    for table in insert_order:
        for file_name, df in df_list:
            if table_mapping.get(file_name) == table:
                proceed = input(f"¿Deseas insertar {file_name} en {table}? (s/n): ")
                if proceed.lower() == 's':
                    insert_df_to_table(df, table)
                    break  # Suponiendo que solo hay un DataFrame por tabla
                else:
                    print(f"No se inserta en {table}")

def print_table_columns():
    """
    Imprime los nombres de las columnas de todas las tablas en la base de datos.
    """
    db = Database()
    cursor = db.conexion.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"\nTabla: {table[0]}")
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 0")
        columns = [desc[0] for desc in cursor.description]
        print("Columnas:", columns)
    cursor.close()
    db.close()

# Ejemplo de uso
if __name__ == "__main__":
    df_list = [(file, make_data_frame(os.path.join(DATA_PATH, file))) for file in NAME_FILES]

    # Crear una nueva lista de tuplas con DataFrames limpios
    clean_df_list = [(df_tuple[0], clean_data_frame(df_tuple[1])) for df_tuple in df_list]

    for file_name, df in clean_df_list:
        print(f'--------------FILE: {file_name}--------------')
        print(df)

        write_clean_data_to_file(CLEAN_DATA_DIR, file_name, df)

    print_table_columns()
    proceed = input("¿Desea continuar con los inserts? (s/n): ")
    if proceed.lower() == 's':
        apply_column_mappings(clean_df_list)
        fix_datatype_columns(clean_df_list)
        insert_in_tables(clean_df_list)
    else:
        print("Operación terminada por el usuario.")

