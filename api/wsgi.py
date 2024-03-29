from flask_cors import CORS
from flask import Flask
from api.controller.controller_client import ClientContoller
from api.controller.controller_employee import EmployeeController

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is not None:
        app.config.update(test_config)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/client')
    def get_clients():
        return ClientContoller().getAllClients()

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

    @app.route('/employee', methods=['POST'])
    def add_employee():
        return EmployeeController().addEmployee()

    @app.route('/employee/<int:eid>', methods=['DELETE'])
    def delete_employee(eid):
        return EmployeeController().deleteEmployee(eid)

    @app.route('/employee/<int:eid>', methods=['PUT'])
    def update_employee(eid):
        return EmployeeController().putEmployee(eid)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

