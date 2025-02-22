import requests

# Replace with your Bluesky handle and password
BLUESKY_HANDLE = 'christyyyyyyy.bsky.social'
PASSWORD = 'gfgt-vazt-kwey-g2pf'

# Endpoint for creating a session
auth_url = 'https://bsky.social/xrpc/com.atproto.server.createSession'

# Payload for authentication
auth_payload = {
    'identifier': BLUESKY_HANDLE,
    'password': PASSWORD
}


# Authenticate and obtain access token
response = requests.post(auth_url, json=auth_payload)
response_data = response.json()

if response.status_code == 200:
    access_token = response_data['accessJwt']
    print("Authentication successful!")
else:
    print("Authentication failed:", response_data)
# Define the keyword to search for
keyword = 'example'

# Endpoint for searching posts
search_url = 'https://bsky.social/xrpc/app.bsky.feed.searchPosts'

# Set up headers with the access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Parameters for the search
params = {
    'q': keyword
}

# Perform the search request
search_response = requests.get(search_url, headers=headers, params=params)
search_results = search_response.json()

if search_response.status_code == 200:
    print(f"\nPosts containing the keyword '{keyword}':")
    print("=" * 50)
    for post in search_results.get('posts', []):
        author = post['author']['handle']
        content = post['record']['text']
        print(f"{author}: {content}\n")
else:
    print("Search failed:", search_results)
