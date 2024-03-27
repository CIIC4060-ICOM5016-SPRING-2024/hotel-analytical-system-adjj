# DB-ADJJ Database credentials

REST API HOSTNAME: https://postgres-app1-075e5eddc52e.herokuapp.com

Host: ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com

Database: ddna4sdma3l2nj

User: u1rgtufv8k5u6r

Port: 5432

Password: p8ddbe35503faf38bad49b9b4847d89cec84b1a019dc2141d016d801ad2d96d50

URI: postgres://u1rgtufv8k5u6r:p8ddbe35503faf38bad49b9b4847d89cec84b1a019dc2141d016d801ad2d96d50@ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddna4sdma3l2nj

Heroku CLI: heroku pg:psql postgresql-objective-43160 --app postgres-app1

# Project Setup
### CSV file with database credentials
When you pull the code you will need to make a csv file called 'credentials'. This will be inside the model folder. Inside the file they will put the database credentials as follows:

![image](https://github.com/CIIC4060-ICOM5016-SPRING-2024/hotel-analytical-system-adjj/assets/95184925/83214ec8-01b5-43a6-a08b-dc98b2246fda)

### It may be necessary to add a path in the system environment variables.
From what I understood when configuring the project, this has to do with importing the python packages. Adding your project's root path to the system's PYTHONPATH is a common practice for solving module import problems in Python, especially in complex projects with a deep directory structure or when working with modules that need to import between subdirectories. If I'm not mistaken, this is not the best solution since it can cause complications when taking the application to production. However, to work locally developing the project logic it is an acceptable solution.

![image](https://github.com/CIIC4060-ICOM5016-SPRING-2024/hotel-analytical-system-adjj/assets/95184925/907459be-68ce-4952-abf6-e402785a148d)

In the name variable you are going to put 'PYTHONPATH' and in the value variable you are going to put the path where your project is located.
![image](https://github.com/CIIC4060-ICOM5016-SPRING-2024/hotel-analytical-system-adjj/assets/95184925/5e6bfaf3-7ce2-4973-97aa-46a3a74ba905)



# Test Driven Development (TDD)
In this project we adopted the TDD (Test-Driven Development) methodology to ensure high code quality and facilitate long-term maintenance. This helps so that with each code update, it can be safely monitored that difficult-to-detect problems or total malfunctions of features have not been caused. Here is how to follow this methodology:

## Step 1: Write the Test
First, before writing any new code for our getAllClients functionality, we start by writing a test that defines what we expect from this functionality. For example, our initial test for getAllClients may look like this:

```python
# tests/test_client_features.py

def test_get_all_clients_initial(client):
    response = client.get('/client')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

```

## Step 2: Write the Minimum Necessary Code
With the test written, the next step is to write the minimum necessary code in our application to make this test pass. At this point, we don't care about implementing all the getAllClients logic, we just want the test to pass.
```python
# app.py o en el archivo correspondiente donde se define el endpoint

@app.route('/client')
def get_all_clients():
    return jsonify([]), 200

```
## Step 3: Implement the Feature and Update the Test
Now that we have a passing test, the next step is to implement the full functionality of getAllClients and, in parallel, update our test to reflect the final requirements for this functionality.
```python
# Implementación final de getAllClients
@app.route('/client')
def get_all_clients():
    clients = ClientDAO.getAllClients()  # Suponiendo que esto devuelve una lista de clientes
    return jsonify(clients), 200

```
And we update our test to verify the structure and data expected from clients:
```python
# Actualización de la prueba para verificar la estructura de los datos
def test_get_all_clients(client):
    response = client.get('/client')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        # Verifica que los campos esperados existan en el primer cliente
        expected_fields = ['age', 'clid', 'fname', 'lname', 'memberyear']
        for field in expected_fields:
            assert field in data[0]
        # Verifica los tipos de datos de los campos
        assert isinstance(data[0]['age'], int)
        assert isinstance(data[0]['clid'], int)
        assert isinstance(data[0]['fname'], str)
        assert isinstance(data[0]['lname'], str)
        assert isinstance(data[0]['memberyear'], int)

```


