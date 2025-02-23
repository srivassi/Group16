import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize sentiment analyzer and Twitter bearer token
analyzer = SentimentIntensityAnalyzer()
bearer_token = os.getenv("BEARER_TOKEN")

def fetch_twitter_posts(keyword, max_results=30):
    """
    Fetch recent tweets matching the keyword.
    Returns a list of tweet entries with text and sentiment.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2RecentSearchPython"
    }
    params = {
        "query": keyword,
        "max_results": max_results,
        "tweet.fields": "created_at,author_id"
    }
    response = requests.get(url, headers=headers, params=params)

    tweets_data = []
    if response.status_code == 200:
        tweets = response.json().get("data", [])
        for tweet in tweets:
            text = tweet.get("text", "")
            sentiment = analyzer.polarity_scores(text)
            tweets_data.append({
                "source": "Twitter",
                "text": text,
                "sentiment": sentiment
            })
    else:
        print("Twitter API error:", response.status_code)
    return tweets_data
