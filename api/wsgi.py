from run import create_app

app = create_app()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/client')
def client():
    return ClientContoller().getAllClients()

if __name__ == '__main__':
    app.run(debug=True)

