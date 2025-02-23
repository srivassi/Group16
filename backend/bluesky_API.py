import os
from atproto import Client
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve Bluesky credentials from environment variables
USERNAME = os.getenv("BLUESKY_API_USERNAME")
PASSWORD = os.getenv("BLUESKY_API_PASSWORD")

# Initialize sentiment analyzer and Bluesky client; login to Bluesky
analyzer = SentimentIntensityAnalyzer()
client = Client()
client.login(USERNAME, PASSWORD)

def fetch_bluesky_posts(keyword, limit=30):
    """
    Fetch posts from Bluesky API that match the keyword.
    Returns a list of posts with text and sentiment scores.
    """
    params = {
        'q': keyword,
        'limit': limit
    }
    posts_data = []
    try:
        response = client.app.bsky.feed.search_posts(params)
        posts = response.posts
        if posts:
            for post in posts:
                text = post.record.text
                sentiment = analyzer.polarity_scores(text)
                posts_data.append({
                    "source": "Bluesky",
                    "text": text,
                    "sentiment": sentiment
                })
    except Exception as e:
        print("Bluesky API Error:", e)
    return posts_data
