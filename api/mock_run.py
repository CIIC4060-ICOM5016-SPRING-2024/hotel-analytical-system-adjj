from api.controller.controller_client import ClientContoller
from flask_cors import CORS
from flask import Flask
  
def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is not None:
        app.config.update(test_config)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/client')
    def client():
        return ClientContoller().getAllClients()

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

