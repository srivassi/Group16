import requests

session = requests.Session()  # Create a persistent session

while True:
    inp = input("André: ")
    url = "http://127.0.0.1:5000/api/chat"
    data = {"query": inp}
    headers = {"Content-Type": "application/json"}
    
    response = session.post(url, json=data, headers=headers)
    print(response.json())