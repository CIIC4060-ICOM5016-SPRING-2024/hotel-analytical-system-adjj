from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px

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

    def graficar_payment_method(self, session):
        url = 'http://127.0.0.1:5000/paymentmethod'
        data = {
            "eid": 3
        }
        response = session.get(url, json=data, verify=False)
        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            # Datos JSON recibidos
            data_json = response.json()
            # Convierte los datos JSON en un DataFrame de pandas
            df = pd.DataFrame(data_json)

            # Gráfico de dona
            fig = px.pie(df, values='percentage_reservations_pay_method', names='payment',
                         title='Porcentaje de Reservas por Método de Pago', hole=0.3)

            # Mejora la visualización con las etiquetas
            fig.update_layout(
                autosize=False,
                width=900,  # Ancho del gráfico
                height=600,  # Altura del gráfico
                margin=dict(l=50, r=50, b=100, t=100, pad=4)  # Ajuste de márgenes
            )

            # Muestra el gráfico
            fig.show()
        else:
            print("Error en la respuesta:", response.status_code)

    def graficar_most_profit_month(self, session):
        url = 'http://127.0.0.1:5000/most/profitmonth'
        data = {"eid": 3}
        response = session.get(url, json=data, verify=False)

        if response.status_code == 200:
            data_json = response.json()
            df = pd.DataFrame(data_json)

            # Convertimos el mes de número a nombre para una mejor visualización
            df['month'] = pd.to_datetime(df['month'], format='%m').dt.strftime('%B')

            # La columna 'size' determinará el tamaño de cada burbuja.
            df['size'] = df['count_reservation']

            # Gráfico de burbujas
            fig = px.scatter(df, x='month', y='chid', size='size', color='count_reservation',
                             hover_name='chid', size_max=60,
                             title='Cantidad de Reservaciones por Mes y CHID')

            # Mejora la visualización con las etiquetas
            fig.update_layout(
                xaxis=dict(title='Mes'),
                yaxis=dict(title='CHID'),
                autosize=False,
                width=900,  # Ancho del gráfico
                height=600,  # Altura del gráfico
            )

            # Muestra el gráfico
            fig.show()
        else:
            print(f"Error en la respuesta: {response.status_code}")
