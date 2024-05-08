from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px

heroku_api = "https://postgres-app1-075e5eddc52e.herokuapp.com"

class GlobalStatsPlots:
    def __init__(self):
        pass

    # def mostrar_graficos_most_reservation(self, session):
    #     url = 'http://127.0.0.1:5000/most/reservation'
    #     data = {
    #         "eid": 3
    #     }
    #     response = session.get(url, json=data, verify=False)
    #     # Verifica si la solicitud fue exitosa
    #     if response.status_code == 200:
    #         # print("Respuesta exitosa")
    #         data_json = response.json()
    #         # Convierte los datos JSON en un DataFrame de pandas
    #         df = pd.DataFrame(data_json)
    #
    #         # Configura el tamaño de la figura
    #         plt.figure(figsize=(10, 6))
    #
    #         # Crea un gráfico de barras
    #         bars = plt.bar(df['hname'], df['reservation_count'], color='skyblue')
    #
    #         # Añade título y etiquetas a los ejes
    #         plt.title('Top 10% de Hoteles con Más Reservaciones')
    #         plt.xlabel('Nombre del Hotel')
    #         plt.ylabel('Número de Reservaciones')
    #
    #         # Rotar las etiquetas del eje X para mejor legibilidad
    #         plt.xticks(rotation=45, ha="right")
    #
    #         # Añade los valores exactos encima de las barras
    #         for bar in bars:
    #             height = bar.get_height()
    #             plt.text(bar.get_x() + bar.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')
    #
    #         # Ajusta el layout para asegurar que las etiquetas no se corten
    #         plt.tight_layout()
    #
    #         # Muestra el gráfico
    #         plt.show()
    #     else:
    #         pass
    #         # print("Error en la respuesta:", response.status_code)

    def mostrar_graficos_most_reservation(self, session):
        # url = 'http://127.0.0.1:5000/most/reservation'
        # data = {"eid": 3}
        url = f"{heroku_api}/most/reservation"
        data = {
            "eid": 3
        }
        response = session.get(url, json=data, verify=False)
        if response.status_code == 200:
            data_json = response.json()
            df = pd.DataFrame(data_json)
            fig = px.bar(df, x='hname', y='reservation_count', title='Top 10% de Hoteles con Más Reservaciones',
                         labels={'hname': 'Nombre del Hotel', 'reservation_count': 'Número de Reservaciones'},
                         color='reservation_count', color_continuous_scale=px.colors.sequential.Viridis)
            fig.update_traces(texttemplate='%{y}', textposition='outside')
            fig.update_layout(autosize=False, width=900, height=600)
            fig.show()
        else:
            print("Error en la respuesta:", response.status_code)


    # def graficar_capacidad_hoteles(self, session):
    #     url = 'http://127.0.0.1:5000/most/capacity'
    #     data = {
    #         "eid": 3
    #     }
    #     response = session.get(url, json=data, verify=False)
    #     # Verifica si la solicitud fue exitosa
    #     if response.status_code == 200:
    #         # print("Respuesta exitosa")
    #         data_json = response.json()
    #         # Convierte los datos JSON en un DataFrame de pandas
    #         df = pd.DataFrame(data_json)
    #
    #         # global_statistic_widget.clear_output(wait=True)  # Limpiamos la salida anterior
    #         plt.figure(figsize=(10, 6))  # Tamaño del gráfico
    #         bars = plt.bar(df['hname'], df['total_capacity'], color='teal')  # Gráfico de barras
    #
    #         # Añadimos etiquetas en las barras
    #         for bar in bars:
    #             yval = bar.get_height()
    #             plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom')
    #
    #         plt.title('Top 5 Hoteles con Mayor Capacidad de Clientes')  # Título del gráfico
    #         plt.xlabel('Nombre del Hotel')  # Etiqueta eje X
    #         plt.ylabel('Capacidad Total')  # Etiqueta eje Y
    #         plt.xticks(rotation=45, ha='right')  # Rotamos las etiquetas para que sean legibles
    #         plt.tight_layout()  # Ajuste del layout
    #         plt.show()

    def graficar_capacidad_hoteles(self, session):
        url = f"{heroku_api}/most/capacity"
        # url = 'http://127.0.0.1:5000/most/capacity'
        data = {"eid": 3}
        response = session.get(url, json=data, verify=False)
        if response.status_code == 200:
            data_json = response.json()
            df = pd.DataFrame(data_json)
            fig = px.bar(df, x='hname', y='total_capacity', title='Top 5 Hoteles con Mayor Capacidad de Clientes',
                         labels={'hname': 'Nombre del Hotel', 'total_capacity': 'Capacidad Total'},
                         color='total_capacity', color_continuous_scale=px.colors.sequential.Plasma)
            fig.update_traces(texttemplate='%{y}', textposition='outside')
            fig.update_layout(autosize=False, width=900, height=600)
            fig.show()
        else:
            print("Error en la respuesta:", response.status_code)

    def graficar_payment_method(self, session):
        # url = 'http://127.0.0.1:5000/paymentmethod'
        url = f"{heroku_api}/paymentmethod"
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
        # url = 'http://127.0.0.1:5000/most/profitmonth'
        url = f"{heroku_api}/most/profitmonth"

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


    def graficar_top_3_chain_with_least_rooms(self, session):
        # url = 'http://127.0.0.1:5000/least/rooms'
        url = f"{heroku_api}/least/rooms"
        data = {"eid": 3}
        response = session.get(url, json=data, verify=False)

        if response.status_code == 200:
            data_json = response.json()
            df = pd.DataFrame(data_json)

            # Ensure that the data is sorted to get the top 3 chains with the least rooms
            df = df.nlargest(3, 'room_count', 'all')

            # Create a simple bar plot for visualization
            fig = px.bar(df, x='chain_name', y='room_count', title='Top 3 Hotel Chains with the Least Rooms',
                         labels={'chain_name': 'Hotel Chain', 'room_count': 'Number of Rooms'},
                         color='room_count',  # Continuous color scale based on the number of rooms
                         color_continuous_scale=px.colors.sequential.Viridis)  # Consistent color palette

            fig.update_layout(
                autosize=False,
                width=900,  # Width of the graph
                height=600,  # Height of the graph
                xaxis_title="Hotel Chain",
                yaxis_title="Number of Rooms"
            )

            # Display the graph
            fig.show()
        else:
            print(f"Error in response: {response.status_code}")

    def graficar_top_3_chains_with_the_highest_total_revenue(self, session):
        # url = 'http://127.0.0.1:5000/most/revenue'  # Endpoint for fetching top 3 chains by revenue
        url = f"{heroku_api}/most/revenue"  # Endpoint for fetching top 3 chains by revenue
        data = {"eid": 3}
        response = session.get(url, json=data, verify=False)

        if response.status_code == 200:
            data_json = response.json()
            df = pd.DataFrame(data_json)

            # Assuming the JSON returns more than 3, we sort and take the top 3 entries
            df = df.nlargest(3, 'total_revenue')

            # Calculate the percentage of total revenue
            total = df['total_revenue'].sum()
            df['percentage_revenue'] = (df['total_revenue'] / total) * 100

            # Gráfico de dona
            fig = px.pie(df, values='percentage_revenue', names='chain_name',
                         title='Top 3 Hotel Chains with the Highest Total Revenue', hole=0.3,
                         hover_data={'total_revenue': ':,.2f'},  # Custom hover text with formatted revenue
                         labels={'percentage_revenue': 'Revenue Share'})

            # Custom hover template to show both percentage and exact revenue
            fig.update_traces(
                hovertemplate='%{label}: <br>Revenue Share: %{percent}<br>Total Revenue: $%{customdata[0]:,}')

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