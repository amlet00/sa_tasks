from requests import delete

print(delete('http://localhost:8080/api/jobs/1').json())

print(delete('http://localhost:8080/api/jobs/999').json())

print(delete('http://localhost:8080/api/jobs/q').json())
