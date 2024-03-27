from api.controller.controller_client import ClientContoller
from flask_cors import CORS
from flask import Flask
  
def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is not None:
        app.config.update(test_config)


    return app


