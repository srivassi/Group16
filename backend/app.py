import os
import requests
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load environment variables if you're using a .env file.
# If you've already set them up in your PyCharm run configuration,
# this call isn't strictly necessary.
load_dotenv()

# Access your credentials from the environment.
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Prepare the request headers.
# For most endpoints, you'll use the Bearer token for authorization.
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "User-Agent": "v2RecentSearchPython"
}

# Define the API endpoint and query parameters.
url = "https://api.twitter.com/2/tweets/search/recent"
analyzer = SentimentIntensityAnalyzer()
tweets_data = []
params = {
    "query": "#MAGICMAN" "#JacksonWang",       # Replace with the hashtag you're interested in.
    "max_results": 30,               # Maximum number of tweets to fetch.
    "tweet.fields": "created_at,author_id"  # Additional tweet details you want returned.
}

# Make the GET request to fetch tweets.
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful.
if response.status_code == 200:
    tweets = response.json().get("data", [])
    for tweet in tweets:
        text = tweet.get("text", "")
        metrics = tweet.get("public_metrics", {})
        sentiment = analyzer.polarity_scores(text)
        tweet_info = {
            "text": text,
            "public_metrics": metrics,
            "sentiment": sentiment
        }
        tweets_data.append(tweet_info)
else:
    print(f"Error: {response.status_code} - {response.text}")


for tweet in tweets_data:
    print("Tweet Text:", tweet["text"])
    print("Public Metrics:", tweet["public_metrics"])
    print("Sentiment:", tweet["sentiment"])
    print("-" * 50)
