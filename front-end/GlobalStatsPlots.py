from matplotlib import pyplot as plt
import pandas as pd

class GlobalStatsPlots:
    def __init__(self):
        pass

    def mostrar_graficos_most_reservation(self, session):
        url = 'http://127.0.0.1:5000/most/reservation'
        data = {
            "eid": 3
        }
        response = session.get(url, json=data, verify=False)
        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            # print("Respuesta exitosa")
            data_json = response.json()
            # Convierte los datos JSON en un DataFrame de pandas
            df = pd.DataFrame(data_json)

            # Configura el tamaño de la figura
            plt.figure(figsize=(10, 6))

            # Crea un gráfico de barras
            bars = plt.bar(df['hname'], df['reservation_count'], color='skyblue')

            # Añade título y etiquetas a los ejes
            plt.title('Top 10% de Hoteles con Más Reservaciones')
            plt.xlabel('Nombre del Hotel')
            plt.ylabel('Número de Reservaciones')

            # Rotar las etiquetas del eje X para mejor legibilidad
            plt.xticks(rotation=45, ha="right")

            # Añade los valores exactos encima de las barras
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

            # Ajusta el layout para asegurar que las etiquetas no se corten
            plt.tight_layout()

            # Muestra el gráfico
            plt.show()
        else:
            pass
            # print("Error en la respuesta:", response.status_code)


    def graficar_capacidad_hoteles(self, session):
        url = 'http://127.0.0.1:5000/most/capacity'
        data = {
            "eid": 3
        }
        response = session.get(url, json=data, verify=False)
        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            # print("Respuesta exitosa")
            data_json = response.json()
            # Convierte los datos JSON en un DataFrame de pandas
            df = pd.DataFrame(data_json)

            # global_statistic_widget.clear_output(wait=True)  # Limpiamos la salida anterior
            plt.figure(figsize=(10, 6))  # Tamaño del gráfico
            bars = plt.bar(df['hname'], df['total_capacity'], color='teal')  # Gráfico de barras

            # Añadimos etiquetas en las barras
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom')

            plt.title('Top 5 Hoteles con Mayor Capacidad de Clientes')  # Título del gráfico
            plt.xlabel('Nombre del Hotel')  # Etiqueta eje X
            plt.ylabel('Capacidad Total')  # Etiqueta eje Y
            plt.xticks(rotation=45, ha='right')  # Rotamos las etiquetas para que sean legibles
            plt.tight_layout()  # Ajuste del layout
            plt.show()