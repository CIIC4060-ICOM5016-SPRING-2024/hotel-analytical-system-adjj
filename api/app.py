from flask import Flask
from flask_cors import CORS
from controller.client import ClientContoller

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/client')
def client():
    return ClientContoller().getAllClients()

if __name__ == '__main__':
    app.run(debug=True)