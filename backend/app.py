import os
import requests
import json
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify
import openai

# Load environment variables from .env or your IDE configuration.
load_dotenv()

app = Flask(__name__)

# Load your credentials for Twitter and OpenAI.
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_tweets():
    """
    Fetches recent tweets matching the query and performs sentiment analysis.
    """
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2RecentSearchPython"
    }
    url = "https://api.twitter.com/2/tweets/search/recent"
    analyzer = SentimentIntensityAnalyzer()
    tweets_data = []
    # Note: Combine hashtags with a space so both are searched.
    params = {
        "query": "#MAGICMAN #JacksonWang",
        "max_results": 30,
        "tweet.fields": "created_at,author_id,public_metrics"
    }
    response = requests.get(url, headers=headers, params=params)
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
    return tweets_data

# Fetch tweets on startup (or you can schedule this periodically).
tweets_data = fetch_tweets()

def get_relevant_tweets(query, tweets):
    """
    Simple filtering: returns tweets where the query string appears in the text.
    """
    query_lower = query.lower()
    return [tweet for tweet in tweets if query_lower in tweet["text"].lower()]

def build_system_prompt(relevant_tweets):
    """
    Builds a system prompt containing the context of relevant tweets and their sentiment.
    """
    if not relevant_tweets:
        context_text = "No tweets were found matching the query."
    else:
        context_text = "\n".join(
            f"Tweet: {tweet['text']} (Sentiment: {tweet['sentiment']})"
            for tweet in relevant_tweets
        )
    system_prompt = (
        "You are a helpful assistant that answers questions based solely on a provided dataset of tweets "
        "and their sentiment scores. Below is the dataset context:\n\n"
        f"{context_text}\n\n"
        "Answer the user's question using only the above information."
    )
    return system_prompt

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Retrieve tweets relevant to the query.
    relevant_tweets = get_relevant_tweets(user_query, tweets_data)
    system_prompt = build_system_prompt(relevant_tweets)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        assistant_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": assistant_reply})
    except Exception as e:
        print("OpenAI API error:", e)
        return jsonify({"error": "Error communicating with OpenAI API"}), 500

if __name__ == '__main__':
    app.run(port=5000)
