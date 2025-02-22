import os
from atproto import Client
from dotenv import load_dotenv

# Initialize the Bluesky API client
load_dotenv()
client = Client()

# Replace with your Bluesky credentials
USERNAME = os.getenv("BLUESKY_API_USERNAME")
PASSWORD = os.getenv("BLUESKY_API_PASSWORD")

# Authenticate the client
client.login(USERNAME, PASSWORD)

# Define the search keyword
keyword = "#Donald"  # Search for posts with this keyword or hashtag

# Optional: Date range filtering (modify as needed)
since_date = "2024-01-01T00:00:00Z"  # Start date (YYYY-MM-DDTHH:MM:SSZ)
until_date = "2024-12-31T23:59:59Z"  # End date (YYYY-MM-DDTHH:MM:SSZ)

# Initialize parameters for the search
params = {
    'q': keyword,
    'limit': 10,  # Number of posts to retrieve per request
    'since': since_date,  # Optional: Start date
    'until': until_date   # Optional: End date
}

# Perform the search with pagination
while True:
    try:
        # Request posts from the Bluesky API
        response = client.app.bsky.feed.search_posts(params)

        # Debug: Print the raw response to inspect structure
        print("Raw Response:", response)

        # Extract posts from response
        posts = response.posts  # Correctly accessing posts attribute

        if posts:
            print(f"Found {len(posts)} posts for '{keyword}':\n")
            for post in posts:
                author = post.author.handle
                content = post.record.text
                timestamp = post.record.created_at
                print(f"Author: {author}\nTime: {timestamp}\nPost: {content}\n{'-'*50}")
        else:
            print("No posts found.")
            break

        # Check for the presence of a cursor for pagination
        if response.cursor:
            params['cursor'] = response.cursor  # Correctly accessing cursor
        else:
            # No more pages to fetch
            break

    except Exception as e:
        print(f"Error: {e}")
        break
