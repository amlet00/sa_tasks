from requests import put, get

print(get('http://localhost:8080/api/jobs').json())

print(put('http://localhost:8080/api/jobs/1',
          json={'job': 'deployment of residential modules 1 and 2',
                'team_leader': 1,
                'work_size': 15,
                'collaborators': '2, 4',
                'is_finished': True}).json())

print(put('http://localhost:8080/api/jobs/999', json={}).json())

print(get('http://localhost:8080/api/jobs').json())
