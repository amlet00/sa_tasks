from requests import post

# корректный запрос:
print(post('http://localhost:8080/api/jobs',
           json={'job': 'deployment of residential modules 1 and 2',
                 'team_leader': 1,
                 'work_size': 15,
                 'collaborators': '2, 3',
                 'is_finished': False}).json())

# пустой запрос
print(post('http://localhost:8080/api/jobs', json={}).json())

# не достаточно полей
print(post('http://localhost:8080/api/jobs',
           json={'job': 'deployment of residential modules 1 and 2'}).json())

# неизвестные поля
print(post('http://localhost:8080/api/jobs',
           json={'title': 'deployment of residential modules 1 and 2',
                 'team_leader': 1,
                 'work_size': 15,
                 'collaborators': '2, 3',
                 'is_finished': False}).json())
