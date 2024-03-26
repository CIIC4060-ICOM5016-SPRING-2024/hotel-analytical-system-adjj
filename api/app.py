from flask import Flask
from flask_cors import CORS
from api.controller.controller_client import ClientContoller
from api.controller.controller_chains import ChainsContoller


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

    @app.route('/chains')
    def chains():
        return ChainsContoller().getAllChains()
    
    @app.route('/chains/<id>')
    def get_chain(id):
        return ChainsContoller().getChain(id)
    
    @app.route('/chains')
    def post_chain():
        return 
    
    @app.route('/chains/:id')
    def put_chain():
        return 
    
    @app.route('/chains/:id')
    def delete_chain():
        return 

    # DONE: 
        # GET:
        #   get all chains
        # GET:
        #     Returns a table element equal to an id as a parameter. Path='/chains/:id'
    # TODO:
        # GET:
        #     Returns a table element equal to an id as a parameter. Path='/chains/:id'
        # POST:
        #     Add a elements to the chains table. Path='/chains'
        # PUT:
        #     Update an element from the chains table by selecting it with an id as a parameter. Path='/chains/:id'
        # DELETE:
        #     Delete an element from the chains table by selecting it with an id as a parameter. Path='chains/:id'

    return app


if __name__ == '__main__':
    create_app().run(debug=True)