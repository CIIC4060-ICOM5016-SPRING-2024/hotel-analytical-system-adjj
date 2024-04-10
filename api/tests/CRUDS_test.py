
import pytest

def test_POST_return_values(client):


    success_employee_response = client.post(f'/employee', json={
        "hid": 17,
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "salary": 32000,
        "position": "Regular"
    })
    success_login_response = client.post(f'/login', json={
        "eid": success_employee_response.get_json()['eid'],
        "username": "test",
        "password": "tS6M@Qnt"
    })
    success_chains_response = client.post(f'/chains', json={
        "cname": "Janiel",
        "fallmkup": 1.1,
        "springmkup": 1.2,
        "summermkup": 1.3,
        "wintermkup": 1.4
    })
    success_hotel_response = client.post(f'/hotel', json={
        "chid": 5,
        "hname": "Hotel de Janiel",
        "hcity": "Mayaguez"
    })
    success_room_response = client.post(f'/room', json={
        "hid": 2,
        "rdid": 20,
        "rprice": 100.50
    })
    success_roomdescription_response = client.post(f'/roomdescription', json={
        "rname": "Standard Queen",
        "rtype": "Premium",
        "capacity": 2,
        "ishandicap": False
    })
    success_roomunavailable_response = client.post(f'/roomunavailable', json={
        "eid": 4,
        "rid": 66,
        "startdate": "2021-01-01",
        "enddate": "2022-01-10"
    })
    success_reserve_response = client.post(f'/reserve', json={
        "ruid":4541,
        "clid":2,
        "payment": "credit card",
        "guests":2,
        "eid" : 1
    })
    success_client_response = client.post(f'/client', json={
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "memberyear": 15
    })

    succes_responsess = [success_chains_response,
                 success_hotel_response,
                 success_employee_response,
                 success_login_response,
                 success_room_response,
                 success_roomdescription_response,
                 success_roomunavailable_response,
                 success_reserve_response,
                 success_client_response]

    print("success_responses:")
    for response in succes_responsess:
        print(response.get_json())

    fail_chains_response = client.post(f'/chains', json={
        "cname": "Janiel",
        "fallmkup": 1.1,
        "springmkup": 1.2,
        "summermkup": 1.3
        #"wintermkup": "1.4"
    })
    fail_hotel_response = client.post(f'/hotel', json={
        "chid": 5,
        "hname": "Hotel de Janiel"
        #"hcity": "Mayaguez"
    })
    fail_employee_response = client.post(f'/employee', json={
        "hid": 17,
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21,
        "salary": 32000
        #"position": "Regular"
    })
    fail_login_response = client.post(f'/login', json={
        "eid": 451,
        "username": "test"
        #"password": "tS6M@Qnt"
    })
    fail_room_response = client.post(f'/room', json={
        "hid": 2,
        "rdid": 20
        #"rprice": 100.50
    })
    fail_roomdescription_response = client.post(f'/roomdescription', json={
        "rname": "Standard Queen",
        "rtype": "Premium",
        "capacity": 2
        #"ishandicap": False
    })
    fail_roomunavailable_response = client.post(f'/roomunavailable', json={
        "eid": 4,
        "rid": 66,
        "startdate": "2021-01-01"
        #"enddate": "2022-01-10"
    })
    fail_reserve_response = client.post(f'/reserve', json={
        "ruid": 4541,
        "clid": 2,
        "payment": "credit card",
        "guests": 2
        #"eid": 1
    })
    fail_client_response = client.post(f'/client', json={
        "fname": "Janiel",
        "lname": "Núñez",
        "age": 21
        #"memberyear": 15
    })

    fail_responses = [fail_chains_response,
                 fail_hotel_response,
                 fail_employee_response,
                 fail_login_response,
                 fail_room_response,
                 fail_roomdescription_response,
                 fail_roomunavailable_response,
                 fail_reserve_response,
                 fail_client_response]

    print("fail_responses:")
    for response in fail_responses:
        print(response.get_json())

    delete_login_response = client.delete(f'/login/{success_login_response.get_json()["lid"]}')
    delete_employee_response = client.delete(f'/employee/{success_employee_response.get_json()["eid"]}')
    delete_chains_response = client.delete(f'/chains/{success_chains_response.get_json()['chid']}')
    delete_hotel_response = client.delete(f'/hotel/{success_hotel_response.get_json()['hid']}')
    delete_room_response = client.delete(f'/room/{success_room_response.get_json()['rid']}')
    delete_roomdescription_response = client.delete(f'/roomdescription/{success_roomdescription_response.get_json()['rdid']}')
    delete_roomunavailable_response = client.delete(f'/roomunavailable/{success_roomunavailable_response.get_json()['ruid']}')
    delete_reserve_response = client.delete(f'/reserve/{success_reserve_response.get_json()['reid']}')
    delete_client_response = client.delete(f'/client/{success_client_response.get_json()['clid']}')

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
        print(response.get_json())
