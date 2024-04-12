
import pytest

def test_POST_return_values(client):

    employee_response = client.post(f'/employee', json={
        "hid": 17,
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "salary": 32000,
        "position": "Regular"
    })
    login_response = client.post(f'/login', json={
        "eid": employee_response.get_json()['id'],
        "username": "test",
        "password": "tS6M@Qnt"
    })
    chains_response = client.post(f'/chains', json={
        "cname": "Janiel",
        "fallmkup": 1.1,
        "springmkup": 1.2,
        "summermkup": 1.3,
        "wintermkup": 1.4
    })
    hotel_response = client.post(f'/hotel', json={
        "chid": 5,
        "hname": "Hotel de Janiel",
        "hcity": "Mayaguez"
    })
    room_response = client.post(f'/room', json={
        "hid": 2,
        "rdid": 20,
        "rprice": 100.50
    })
    roomdescription_response = client.post(f'/roomdescription', json={
        "rname": "Standard Queen",
        "rtype": "Premium",
        "capacity": 2,
        "ishandicap": False
    })
    roomunavailable_response = client.post(f'/roomunavailable', json={
        "eid": 4,
        "rid": 66,
        "startdate": "2021-01-01",
        "enddate": "2022-01-10"
    })
    reserve_response = client.post(f'/reserve', json={
        "ruid":4541,
        "clid":2,
        "payment": "credit card",
        "guests":2,
        "eid" : 1
    })
    client_response = client.post(f'/client', json={
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "memberyear": 15
    })

    responsess = [chains_response,
                 hotel_response,
                 employee_response,
                 login_response,
                 room_response,
                 roomdescription_response,
                 roomunavailable_response,
                 reserve_response,
                 client_response]

    print("Success_responses:")
    for response in responsess:
        res = response.get_json()
        print("Status: " + res['status'], "Message: " + res['message'], "Id: " + str(res['id']))

    delete_login_response = client.delete(f'/login/{login_response.get_json()["id"]}')
    delete_employee_response = client.delete(f'/employee/{employee_response.get_json()["id"]}')
    delete_chains_response = client.delete(f'/chains/{chains_response.get_json()['id']}')
    delete_hotel_response = client.delete(f'/hotel/{hotel_response.get_json()['id']}')
    delete_room_response = client.delete(f'/room/{room_response.get_json()['id']}')
    delete_roomdescription_response = client.delete(f'/roomdescription/{roomdescription_response.get_json()['id']}')
    delete_roomunavailable_response = client.delete(f'/roomunavailable/{roomunavailable_response.get_json()['id']}')
    delete_reserve_response = client.delete(f'/reserve/{reserve_response.get_json()['id']}')
    delete_client_response = client.delete(f'/client/{client_response.get_json()['id']}')

    delete_responses = [delete_employee_response,
                      delete_login_response,
                      delete_chains_response,
                      delete_hotel_response,
                      delete_room_response,
                      delete_roomdescription_response,
                      delete_roomunavailable_response,
                      delete_reserve_response,
                      delete_client_response]

    print("Delete Complete:")
    for response in delete_responses:
        res = response.get_json()
        print("Status: " + res['status'], "Message: " + res['message'])
