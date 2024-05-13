from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import requests

load_dotenv()

env = os.getenv('ENV')
# print("Environment:",env)

session = requests.Session()

if (env == 'development'):
    api = "http://127.0.0.1:5000"
elif(env == 'production'):
    api = "https://postgres-app1-075e5eddc52e.herokuapp.com"

# print("API: ", api)

class LocalStatsPlots:
    def __init__(self):
        pass

    # def graficar_top_3_highest_pais_regular_employees(self, session, json, hid):
    #     # Endpoint y cuerpo de la petición
    #     url = f'http://127.0.0.1:5000/hotel/{hid}/highestpaid'
    #
    #     # Realizamos la petición al endpoint
    #     respuesta = session.get(url, json=json)
    #
    #     # Verificamos si la petición fue exitosa
    #     if respuesta.status_code == 200:
    #         datos = respuesta.json()
    #
    #         # Convertimos los datos a DataFrame
    #         df = pd.DataFrame(datos)
    #
    #         # Creamos la gráfica
    #         plt.figure(figsize=(10, 6))
    #         bars = plt.barh(df['fname'] + ' ' + df['lname'], df['salary'], color='skyblue')
    #         plt.xlabel('Salario')
    #         plt.title('Top 3 Empleados Regulares Mejor Pagados')
    #
    #         for bar in bars:
    #             width = bar.get_width()
    #             plt.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.2f}', va='center')
    #
    #         plt.tight_layout()
    #
    #         # Mostramos la gráfica
    #         plt.show()
    #     else:
    #         print("Error al obtener los datos")

    def graficar_top_3_highest_pais_regular_employees(self, session, json, hid):
        # url = f'http://127.0.0.1:5000/hotel/{hid}/highestpaid'
        # Endpoint y cuerpo de la petición
        url = f"{api}/hotel/{hid}/highestpaid"


        # Realizamos la petición al endpoint
        respuesta = session.get(url, json=json)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            df = pd.DataFrame(datos)
            fig = px.bar(df, x='salary', y=df['fname'] + ' ' + df['lname'], orientation='h',
                         title='Top 3 Empleados Regulares Mejor Pagados', labels={'x': 'Salario', 'y': 'Nombre'},
                         color='salary', color_continuous_scale='Tealgrn')
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')
            fig.update_layout(autosize=False, width=900, height=600)
            fig.show()
        else:
            print("Error al obtener los datos")

    # def graficar_top_5_clientes_jovenes_con_mas_reservaciones(self, session, hid, json):
    #     # Suponiendo que puedes pasar eid como un parámetro en la URL
    #     url = f'http://127.0.0.1:5000/hotel/{hid}/mostcreditcard'
    #
    #     # Realizamos la petición al endpoint
    #     respuesta = session.get(url, json=json)
    #
    #     # Verificamos si la petición fue exitosa
    #     if respuesta.status_code == 200:
    #         datos = respuesta.json()
    #
    #         # Convertimos los datos a DataFrame
    #         df = pd.DataFrame(datos)
    #
    #         # Creamos la gráfica
    #         plt.figure(figsize=(10, 6))
    #         plt.barh(df['fname'] + ' ' + df['lname'], df['reservation_count'], color='teal')
    #         plt.xlabel('Cantidad de Reservaciones')
    #         plt.title('Top 5 Clientes Menores de 30 Años con Más Reservaciones con Tarjeta de Crédito')
    #
    #         # Añadiendo los valores exactos en cada barra
    #         for bar in plt.barh(df['fname'] + ' ' + df['lname'], df['reservation_count']):
    #             width = bar.get_width()
    #             plt.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center')
    #
    #         plt.tight_layout()
    #
    #         # Mostramos la gráfica
    #         plt.show()
    #     else:
    #         print("Error al obtener los datos")

    def graficar_top_5_clientes_jovenes_con_mas_reservaciones(self, session, hid, json):
        # url = f'http://127.0.0.1:5000/hotel/{hid}/mostcreditcard'
        # Suponiendo que puedes pasar eid como un parámetro en la URL
        url = f"{api}/hotel/{hid}/mostcreditcard"

        # Realizamos la petición al endpoint
        respuesta = session.get(url, json=json)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            df = pd.DataFrame(datos)
            fig = px.bar(df, x='reservation_count', y=df['fname'] + ' ' + df['lname'], orientation='h',
                         title='Top 5 Clientes Menores de 30 Años con Más Reservaciones con Tarjeta de Crédito',
                         labels={'x': 'Cantidad de Reservaciones', 'y': 'Nombre'},
                         color='reservation_count', color_continuous_scale='Tealgrn')
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')
            fig.update_layout(autosize=False, width=900, height=600)
            fig.show()
        else:
            print("Error al obtener los datos")
    def graficar_top_3_cuartos_reservados_con_menos_gtc_ratio(self,session,hid,json):
        url = f"{api}/hotel/{hid}/leastguests"
        respuesta = session.get(url, json=json)
        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()
            # Verify if data has the expected format
            if not datos or not all('avg_guest_to_capacity_ratio' in d and 'rid' in d for d in datos):
                print("Incomplete or incorrect data.")
                return
            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            fig = px.bar(df, y='rid', x='avg_guest_to_capacity_ratio', orientation='h',
                         text='avg_guest_to_capacity_ratio',
                         title="Top 3 Rooms Reserved with the Least Guest-to-Capacity Ratio",
                         labels={'rname': 'Room Name',
                                 'avg_guest_to_capacity_ratio': 'Average Guest-to-Capacity Ratio'},
                         color='avg_guest_to_capacity_ratio',
                         color_continuous_scale='Tealgrn')  # Use a teal-green color scale

            # Customizing hover data to show more details
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Room Name: %{y}",
                    "Avg. Guest-to-Capacity Ratio: %{x:.2f}"
                ])
            )

            # Enhance the layout
            fig.update_layout(
                xaxis_title='Average Guest-to-Capacity Ratio',
                yaxis_title='Room Name',
                yaxis=dict(type='category'),
                coloraxis_colorbar=dict(
                    title='GTC Ratio'
                )
            )

            # Ensure text is always displayed on the bars
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')

            fig.show()
        else:
            print("Error al obtener los datos")
    def graficar_total_reservation_by_room_type(self,session,hid,json):
        url = f"{api}/hotel/{hid}/roomtype"
        respuesta = session.get(url, json=json)
        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

        if respuesta.status_code == 200:
            data = respuesta.json()

            df = pd.DataFrame(data)

            fig = px.bar(df, x='rtype',y='total_reservations', orientation='v',
                         title='Total reservation by room type.',
                         labels={'total_reservations':'Total Reservations', 'rtype':'Room Type'},
                         color='total_reservations', color_continuous_scale='Tealgrn')
            # Creamos la gráfica
            fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
            fig.update_layout(autosize=False, width=800, height=600)
            fig.show()
 
        else:
            print("Error al obtener los datos")
    def graficar_top_5_clients_received_the_most_discounts(self,session,hid,json):
        url = f"{api}/hotel/{hid}/mostdiscount"
        respuesta = session.get(url, json=json)
        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

        if respuesta.status_code == 200:
            data = respuesta.json()

            if not data or not all('discount_percentage' in d and 'fname' in d and 'lname' in d for d in data):
                print("Incomplete or incorrect data.")
                return

            df = pd.DataFrame(data)

            # Creating a horizontal bar chart
            fig = px.bar(df, y=df['fname'] + ' ' + df['lname'], x='discount_percentage', orientation='h',
                         text='discount_percentage', title="Top 5 Clients That Received the Most Discounts",
                         labels={'fname lname': 'Client Name', 'discount_percentage': 'Discount'},
                         color='discount_percentage', color_continuous_scale='Tealgrn')  # Use a teal-green color scale
             # Customizing hover data to show more details
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Client Name: %{y}",
                    "Discount Percentage: %{x}%"
                ])
            )

            # Enhance the layout
            fig.update_layout(
                xaxis_title='Discount Percentage',
                yaxis_title='Client Name',
                yaxis=dict(type='category'),
                coloraxis_colorbar=dict(
                    title='Discount'
                )
            )

            # Ensure text is always displayed on the bars
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')


            # fig.update_yaxes(range=[0,50])
            fig.show()
        else:
            print("Error fetching data: HTTP Status", respuesta.status_code)

    def graficar_top_3_rooms_with_least_reservation(self, session, hid, json):
        # url = f'http://127.0.0.1:5000/hotel/{hid}/leastreserve'
        url = f'{api}/hotel/{hid}/leastreserve'
        respuesta = session.get(url, json=json)

        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Verificamos si los datos tienen el formato esperado
            if not datos or not all('reserved days' in d and 'rid' in d for d in datos):
                print("Datos incompletos o incorrectos.")
                return

            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            # Creamos la gráfica de barras horizontales
            fig = px.bar(df, y='rid', x='reserved days', orientation='h',
                         text='reserved days', title="Top 3 rooms that were the least time unavailable.",
                         labels={'rid': 'Room ID', 'reserved days': 'Reserved Days'},
                         color='reserved days', color_continuous_scale='Tealgrn')

            # Mejoramos el layout
            fig.update_layout(
                xaxis_title='Reserved Days',
                yaxis_title='Room ID',
                yaxis=dict(type='category'),
                coloraxis_colorbar=dict(
                    title='Reserved Days'
                )
            )

            # Hacer que los textos se muestren siempre en las barras
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')

            # Mostramos la gráfica
            fig.show()
        else:
            print("Error al obtener los datos: HTTP Status", respuesta.status_code)

    def graficar_top_5_handicap_rooms_most_reserved(self, session, hid, json):
        # url = f'http://127.0.0.1:5000/hotel/{hid}/handicaproom'  # Adjust the endpoint as necessary
        url = f'{api}/hotel/{hid}/handicaproom'  # Adjust the endpoint as necessary

        response = session.get(url, json=json)

        if response.status_code == 200:
            data = response.json()

            # Print the data for debugging
            # print("Data received:", data)

            # Verify if data has the expected format
            if not data or not all('reservation_count' in d and 'room_id' in d for d in data):
                print("Incomplete or incorrect data.")
                return

            df = pd.DataFrame(data)



            # Creating a horizontal bar chart
            fig = px.bar(df, y='room_id', x='reservation_count', orientation='h',
                         text='reservation_count', title="Top 5 Handicap-Accessible Rooms Most Reserved",
                         labels={'room_id': 'Room ID', 'reservation_count': 'Number of Reservations',
                                 'room_name': 'Room Name', 'room_type': 'Room Type'},
                         color='reservation_count', color_continuous_scale='Tealgrn')  # Use a teal-green color scale

            # Customizing hover data to show more details
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Room ID: %{y}",
                    "Room Name: %{customdata[0]}",
                    "Room Type: %{customdata[1]}",
                    "Reservations: %{x}"
                ]),
                customdata=df[['room_name', 'room_type']]
            )

            # Enhance the layout
            fig.update_layout(
                xaxis_title='Number of Reservations',
                yaxis_title='Room ID',
                yaxis=dict(type='category'),
                coloraxis_colorbar=dict(
                    title='Number of Reservations'
                )
            )

            # Ensure text is always displayed on the bars
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')

            # Display the chart
            fig.show()
        else:
            print("Error fetching data: HTTP Status", response.status_code)

