import requests

baseUrl = "http://127.0.0.1:5000/"

response = requests.get(baseUrl + "/getCourse/INF5151")
print(response.json())