from flask_cors import CORS
from flask import Flask
from api.controller.controller_client import ClientContoller
from api.controller.controller_employee import EmployeeController
from api.controller.controller_hotel import HotelContoller
from api.controller.controller_chains import ChainsContoller

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

    @app.route('/hotel/<int:hid>/highestpaid')
    def getTopPaidRegularEmployeesByHotel(hid):
        return EmployeeController().getTopPaidRegularEmployeesByHotel(hid)

    @app.route('/hotel/<int:hid>/mostcreditcard')
    def getTop5CreditCardReservations(hid):
        return ClientContoller().getTop5CreditCardReservations(hid)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

