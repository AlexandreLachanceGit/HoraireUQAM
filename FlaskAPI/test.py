import requests

baseUrl = "http://127.0.0.1:5000/"

response = requests.get(baseUrl + "getCourses/INF1132,INF1120,INF1070,MET1110,ECO1081,INF2171,INF2120,MAT4681,INF2050,INF3271,INF3190,INF3080,INF3135,INF5151,INF3173,INF3105,INF5153,INF5130,INM5151,INF6150,INF6120,INM6000,INF4170-a21")
print(response.json())