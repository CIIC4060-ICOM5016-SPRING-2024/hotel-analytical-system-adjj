from matplotlib import pyplot as plt
import pandas as pd

class LocalStatsPlots:
    def __init__(self):
        pass

    def graficar_top_3_highest_pais_regular_employees(self, session, json, hid):
        # Endpoint y cuerpo de la petición
        url = f'http://127.0.0.1:5000/hotel/{hid}/highestpaid'


        # Realizamos la petición al endpoint
        respuesta = session.get(url, json=json)

        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            # Creamos la gráfica
            plt.figure(figsize=(10, 6))
            bars = plt.barh(df['fname'] + ' ' + df['lname'], df['salary'], color='skyblue')
            plt.xlabel('Salario')
            plt.title('Top 3 Empleados Regulares Mejor Pagados')

            for bar in bars:
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.2f}', va='center')

            plt.tight_layout()

            # Mostramos la gráfica
            plt.show()
        else:
            print("Error al obtener los datos")

    def graficar_top_5_clientes_jovenes_con_mas_reservaciones(self, session, hid, json):
        # Suponiendo que puedes pasar eid como un parámetro en la URL
        url = f'http://127.0.0.1:5000/hotel/{hid}/mostcreditcard'

        # Realizamos la petición al endpoint
        respuesta = session.get(url, json=json)

        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            # Creamos la gráfica
            plt.figure(figsize=(10, 6))
            plt.barh(df['fname'] + ' ' + df['lname'], df['reservation_count'], color='teal')
            plt.xlabel('Cantidad de Reservaciones')
            plt.title('Top 5 Clientes Menores de 30 Años con Más Reservaciones con Tarjeta de Crédito')

            # Añadiendo los valores exactos en cada barra
            for bar in plt.barh(df['fname'] + ' ' + df['lname'], df['reservation_count']):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center')

            plt.tight_layout()

            # Mostramos la gráfica
            plt.show()
        else:
            print("Error al obtener los datos")
    def graficar_top_3_cuartos_reservados_con_menos_gtc_ratio(self,session,hid,json):
        url = f'http://127.0.0.1:5000/hotel/{hid}/leastguests'
        respuesta = session.get(url, json=json)
        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            # Creamos la gráfica
            plt.figure(figsize=(10, 6))
            plt.barh(df['rname'], df['avg_guest_to_capacity_ratio'], color='teal')
            plt.xlabel('Average Guest-to-Capacity Ratio')
            plt.title("Top 3 rooms reserved that had the least guest-to-capacity ratio")

            # Añadiendo los valores exactos en cada barra
            for bar in plt.barh(df['rname'], df['avg_guest_to_capacity_ratio']):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center')

            plt.tight_layout()

            # Mostramos la gráfica
            plt.show()
        else:
            print("Error al obtener los datos")
    def graficar_total_reservation_by_room_type(self,session,hid,json):
        url = f'http://127.0.0.1:5000/hotel/{hid}/roomtype'
        respuesta = session.get(url, json=json)
        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            # Creamos la gráfica
            plt.figure(figsize=(10, 6))
            plt.barh(df['rtype'], df['total_reservations'], color='teal')
            plt.xlabel('Total Reservations')
            plt.title("Total reservation by room type.")

            # Añadiendo los valores exactos en cada barra
            for bar in plt.barh(df['rtype'], df['total_reservations']):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center')

            plt.tight_layout()

            # Mostramos la gráfica
            plt.show()
        else:
            print("Error al obtener los datos")
    def graficar_top_5_clients_received_the_most_discounts(self,session,hid,json):
        url = f'http://127.0.0.1:5000/hotel/{hid}/mostdiscount'
        respuesta = session.get(url, json=json)
        # Verificamos si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Convertimos los datos a DataFrame
            df = pd.DataFrame(datos)

            # Creamos la gráfica
            plt.figure(figsize=(10, 6))
            plt.barh(df['fname'] + ' ' + df['lname'], df['discount_percentage'], color='teal')
            plt.xlabel('Discount')
            plt.title("Top 5 clients that received the most discounts")

            # Añadiendo los valores exactos en cada barra
            for bar in plt.barh(df['fname'] + ' ' + df['lname'],df['discount_percentage']):
                width = bar.get_width()
                plt.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center')

            plt.tight_layout()

            # Mostramos la gráfica
            plt.show()
        else:
            print("Error al obtener los datos")



