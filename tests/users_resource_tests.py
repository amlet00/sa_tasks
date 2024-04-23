import requests

print(requests.get('http://localhost:8080/api/v2/users').json())

print(requests.get('http://localhost:8080/api/v2/users/1').json())

print(requests.get('http://localhost:8080/api/v2/users/999').json())

print(requests.post('http://localhost:8080/api/v2/users',
                    json={'surname': 'Qwe',
                          'name': 'Rty',
                          'age': 123,
                          'position': 'asd',
                          'speciality': 'fgh',
                          'address': 'zxc',
                          'email': 'vbn',
                          'password': '123'}).json())

print(requests.post('http://localhost:8080/api/v2/users', json={}).json())

print(requests.post('http://localhost:8080/api/v2/users',
                    json={'surname': 'Qwe'}).json())

print(requests.delete('http://localhost:8080/api/v2/users/5').json())

print(requests.delete('http://localhost:8080/api/v2/users/999').json())
