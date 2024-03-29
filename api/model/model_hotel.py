from .db import Database
class HotelDAO:
    def __init__(self):
        self.db = Database()

    def getAllHotels(self):
        cur = self.db.conexion.cursor()
        query = "SELECT hid, chid, hname, hcity  FROM hotel"
        cur.execute(query)
        hotel_list = cur.fetchall()
        self.db.close()
        cur.close()

        return hotel_list