import requests

#This is a testing file, it is used to test the requests from the app.py file

session = requests.Session()  # Create a persistent session

# First, send a keyword to the /api/getPosts endpoint
keyword = input("Enter a keyword to fetch posts: ")
url_get_posts = "http://127.0.0.1:5000/api/getPosts"
data_get_posts = {"keyword": keyword}
headers = {"Content-Type": "application/json"}

response_get_posts = session.post(url_get_posts, json=data_get_posts, headers=headers)
print("Posts fetched:", response_get_posts.json())

while True:
    inp = input("André: ")
    url_chat = "http://127.0.0.1:5000/api/chat"
    data_chat = {"query": inp}
    
    response_chat = session.post(url_chat, json=data_chat, headers=headers)
    print(response_chat.json())