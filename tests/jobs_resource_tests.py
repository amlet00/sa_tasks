import requests

print(requests.get('http://localhost:8080/api/v2/jobs').json())

print(requests.get('http://localhost:8080/api/v2/jobs/1').json())

print(requests.get('http://localhost:8080/api/v2/jobs/999').json())

print(requests.post('http://localhost:8080/api/v2/jobs',
                    json={'team_leader': 1,
                          'job': 'qwe',
                          'work_size': 123,
                          'collaborators': '2, 3',
                          'is_finished': False
                          }).json())

print(requests.post('http://localhost:8080/api/v2/jobs', json={}).json())

print(requests.post('http://localhost:8080/api/v2/jobs',
                    json={'surname': 'Qwe'}).json())

print(requests.delete('http://localhost:8080/api/v2/jobs/5').json())

print(requests.delete('http://localhost:8080/api/v2/jobs/999').json())
