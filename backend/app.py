import os
import json
import requests
from atproto import Client
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load environment variables
load_dotenv()

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API credentials
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Bluesky API credentials
USERNAME = os.getenv("BLUESKY_API_USERNAME")
PASSWORD = os.getenv("BLUESKY_API_PASSWORD")

# Initialize Bluesky client
client = Client()
client.login(USERNAME, PASSWORD)


# Function to fetch tweets from Twitter API
def fetch_twitter_posts(keyword, max_results=100):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}", "User-Agent": "v2RecentSearchPython"}
    params = {"query": keyword, "max_results": max_results, "tweet.fields": "created_at,author_id"}
    response = requests.get(url, headers=headers, params=params)

    tweets_data = []
    if response.status_code == 200:
        tweets = response.json().get("data", [])
        for tweet in tweets:
            text = tweet.get("text", "")
            sentiment = analyzer.polarity_scores(text)
            tweets_data.append({"source": "Twitter", "text": text, "sentiment": sentiment})
    return tweets_data


# Function to fetch posts from Bluesky API
def fetch_bluesky_posts(keyword, limit=100):
    params = {'q': keyword, 'limit': limit}
    posts_data = []

    try:
        response = client.app.bsky.feed.search_posts(params)
        posts = response.posts
        if posts:
            for post in posts:
                text = post.record.text
                sentiment = analyzer.polarity_scores(text)
                posts_data.append({"source": "Bluesky", "text": text, "sentiment": sentiment})
    except Exception as e:
        print(f"Bluesky API Error: {e}")
    return posts_data


# Main execution
keyword = "Pope Francis"  # Change the keyword if needed

# Fetch posts from both sources
twitter_posts = fetch_twitter_posts(keyword, max_results=100)
bluesky_posts = fetch_bluesky_posts(keyword, limit=100)

# Combine results
all_posts = twitter_posts + bluesky_posts

# Calculate aggregate sentiment score
if all_posts:
    total_compound = sum(post["sentiment"]["compound"] for post in all_posts)
    avg_compound = total_compound / len(all_posts)
    aggregate_sentiment = ((avg_compound + 1) / 2) * 100  # Convert to 0-100 scale
else:
    aggregate_sentiment = None

# Save results to JSON
output_data = {
    "keyword": keyword,
    "aggregate_sentiment": aggregate_sentiment,
    "posts": all_posts
}

with open("sentiment_results.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

# Print summary
print(f"Aggregate Sentiment Score: {aggregate_sentiment}")
print(f"Total Posts Analyzed: {len(all_posts)}")
