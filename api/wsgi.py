from flask_cors import CORS
from flask import Flask
from api.controller.controller_client import ClientContoller
from api.controller.controller_employee import EmployeeController
from api.controller.controller_hotel import HotelContoller
from api.controller.controller_chains import ChainsContoller
from api.controller.controller_room import RoomController
from api.controller.controller_roomunavailable import RoomUnavailableController
from api.controller.controller_login import LoginController
from api.controller.controller_roomdescription import RoomDescriptionController
from api.controller.controller_reserve import ReserveController

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is not None:
        app.config.update(test_config)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/chains')
    def get_chains():
        return ChainsContoller().getAllChains()

    @app.route('/chains/<int:chid>')
    def get_chain(chid):
        return ChainsContoller().getChain(chid)

    @app.route('/chains', methods=['POST'])
    def add_chain():
        return ChainsContoller().addChain()
    @app.route('/chains/<int:chid>', methods=['DELETE'])
    def delete_chain(chid):
        return ChainsContoller().deleteChain(chid)

    @app.route('/chains/<int:chid>', methods=['PUT'])
    def update_chain(chid):
        return ChainsContoller().putChain(chid)

    @app.route('/client')
    def get_clients():
        return ClientContoller().getAllClients()

    @app.route('/client/<int:clid>')
    def get_client(clid):
        return ClientContoller().getClientById(clid)

    @app.route('/client', methods=['POST'])
    def add_client():
        return ClientContoller().addEmployee()

    @app.route('/client/<int:clid>', methods=['DELETE'])
    def delete_client(clid):
        return ClientContoller().deleteClient(clid)

    @app.route('/client/<int:clid>', methods=['PUT'])
    def update_client(clid):
        return ClientContoller().putClient(clid)
    

    @app.route('/employee')
    def get_employees():
        return EmployeeController().getAllEmployees()

    @app.route('/employee/<int:eid>')
    def get_employee(eid):
        return EmployeeController().getEmployeeById(eid)

    @app.route('/employee', methods=['POST'])
    def add_employee():
        return EmployeeController().addEmployee()

    @app.route('/employee/<int:eid>', methods=['DELETE'])
    def delete_employee(eid):
        return EmployeeController().deleteEmployee(eid)

    @app.route('/employee/<int:eid>', methods=['PUT'])
    def update_employee(eid):
        return EmployeeController().putEmployee(eid)

    @app.route('/hotel')
    def get_hotels():
        return HotelContoller().getAllHotels()

    @app.route('/hotel/<int:hid>')
    def get_hotel(hid):
        return HotelContoller().getHotelById(hid)

    @app.route('/hotel', methods=['POST'])
    def add_hotel():
        return HotelContoller().addHotel()

    @app.route('/hotel/<int:hid>', methods=['DELETE'])
    def delete_hotel(hid):
        return HotelContoller().deleteHotel(hid)

    @app.route('/hotel/<int:hid>', methods=['PUT'])
    def update_hotel(hid):
        return HotelContoller().putHotel(hid)

    @app.route('/most/reservation')
    def get_most_reservations():
        return HotelContoller().get_most_reservations()

    @app.route('/most/capacity')
    def get_most_capacity():
        return HotelContoller().get_most_capacity()
    
    @app.route('/hotel/<int:hid>/roomtype',methods=['GET'])
    def get_total_reservations_by_room_type(hid):
        return HotelContoller().get_total_reservations_by_room_type(hid)

    @app.route('/hotel/<int:hid>/highestpaid')
    def getTopPaidRegularEmployeesByHotel(hid):
        return EmployeeController().getTopPaidRegularEmployeesByHotel(hid)

    @app.route('/hotel/<int:hid>/mostcreditcard')
    def getTop5CreditCardReservations(hid):
        return ClientContoller().getTop5CreditCardReservations(hid)
    
    @app.route('/hotel/<int:hid>/mostdiscount',methods=['GET'])
    def getTop5ClientsMostDiscount(hid):
        return ClientContoller().getTop5ClientsMostDiscount(hid)


    @app.route('/room')
    def get_rooms():
        return RoomController().getAllRooms()

    @app.route('/room/<int:rid>')
    def get_room(rid):
        return RoomController().getRoomById(rid)

    @app.route('/room', methods=['POST'])
    def post_room():
        return RoomController().postRoom()

    @app.route('/room/<int:rid>', methods=['DELETE'])
    def delete_room(rid):
        return RoomController().deleteRoom(rid)

    @app.route('/room/<int:rid>', methods=['PUT'])
    def put_room(rid):
        return RoomController().putRoom(rid)

    @app.route('/roomunavailable')
    def get_rooms_unavailable():
        return RoomUnavailableController().getAllRoomsUnavailable()

    @app.route('/roomunavailable/<int:ruid>')
    def get_room_available(ruid):
        return RoomUnavailableController().getRoomUnavailableById(ruid)

    @app.route('/roomunavailable', methods=['POST'])
    def post_room_unavailable():
        return RoomUnavailableController().postRoomUnavailable()

    @app.route('/roomunavailable/<int:ruid>', methods=['DELETE'])
    def delete_room_unavailable(ruid):
        return RoomUnavailableController().deleteRoomUnavailable(ruid)

    @app.route('/roomunavailable/<int:ruid>', methods=['PUT'])
    def put_room_unavailable(ruid):
        return RoomUnavailableController().putRoomUnavailable(ruid)


##############################################

    @app.route('/login')
    def get_logins():
        return LoginController().getAllLogins()

    @app.route('/login/<int:lid>')
    def get_login(lid):
        return LoginController().getLoginById(lid)

    @app.route('/login/<int:lid>', methods=['PUT'])
    def update_login(lid):
        return LoginController().putLogin(lid)
    @app.route('/login/<int:lid>', methods=['DELETE'])
    def delete_login(lid):
        return LoginController().deleteEmployee(lid)

    @app.route('/login', methods=['POST'])
    def add_login():
        return LoginController().addLogin()


    @app.route('/roomdescription')
    def get_RoomsDescriptions():
        return RoomDescriptionController().getAllRoomDescriptions()

    @app.route('/roomdescription/<int:rdid>')
    def get_RoomsDescription(rdid):
        return RoomDescriptionController().getRoomsDescriptionById(rdid)

    @app.route('/roomdescription', methods=['POST'])
    def add_roomdescription():
        return RoomDescriptionController().addRoomDescription()
    #
    @app.route('/roomdescription/<int:rdid>', methods=['DELETE'])
    def delete_roomdescription(rdid):
        return RoomDescriptionController().deleteRoomDescription(rdid)
    @app.route('/roomdescription/<int:rdid>', methods=['PUT'])
    def update_roomdescription(rdid):
        return RoomDescriptionController().putRoomDescription(rdid)

    @app.route('/reserve')
    def get_all_reservations():
        return ReserveController().getAllReservations()
    @app.route('/reserve/<int:reid>')
    def get_reservation(reid):
        return ReserveController().getReservation(reid)

    @app.route('/reserve',methods=['POST'])
    def add_reservation():
        return ReserveController().addReservation()

    @app.route('/reserve/<int:reid>', methods=['PUT'])
    def update_reservation(reid):
        return ReserveController().putReservation(id=reid)

    @app.route('/reserve/<int:reid>', methods=['DELETE'])
    def delete_reservation(reid):
        return ReserveController().deleteReservation(id=reid)


    @app.route('/hotel/<int:hid>/leastreserve', methods=['GET'])
    def get_top_3_rooms_least_unavailable(hid):
        return RoomUnavailableController().getTop3LeastUnavailable(hid)
    
    @app.route('/hotel/<int:hid>/leastguests', methods=['GET'])
    def get_top3_rooms_least_gc_ratio(hid):
        return ReserveController().getTop3RoomsLeastGuestCapacity(hid)

    @app.route('/paymentmethod', methods=['GET'])
    def get_payment_methods():
        return ReserveController().getReserveByPayMethod()

    @app.route('/most/profitmonth', methods=['GET'])
    def get_most_profit_month():
        return ChainsContoller().getTop3ProfitMonthsByChain()


    @app.route('/least/rooms')
    def get_chains_least_rooms():
        return ChainsContoller().get_least_rooms_chains()

    @app.route('/most/revenue')
    def get_chains_highest_revenue():
        return ChainsContoller().get_highest_revenue_chains()

    @app.route('/hotel/<int:hid>/handicaproom', methods=['GET'])
    def get_top_5_handicap_reserved_rooms(hid):
        return RoomController().get_top_5_handicap_reserved(hid)

  

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

