from flask_cors import CORS
from flask import Flask
from api.controller.controller_client import ClientContoller
from api.controller.controller_employee import EmployeeContoller

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


    @app.route('/employee')
    def get_employees():
        return EmployeeContoller().getAllEmployees()

    @app.route('/employee', methods=['POST'])
    def add_employee():
        return EmployeeContoller().addEmployee()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

