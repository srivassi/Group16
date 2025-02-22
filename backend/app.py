import os
import requests
import json
from atproto import Client
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify, session
import openai
from datetime import timedelta

OpenAI = openai.OpenAI

# Load environment variables from .env or your IDE configuration.
load_dotenv()

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
# Use a fixed secret key from the environment or default (ensure to set FLASK_SECRET_KEY in production)
app.secret_key = app.secret_key = os.urandom(24)
# Optionally set a permanent session lifetime (here, 7 days)
app.permanent_session_lifetime = timedelta(days=7)

# Load your credentials for Twitter and OpenAI.
api_key = os.getenv("API_KEY_TWITTER")
api_secret = os.getenv("API_SECRET_TWITTER")
bearer_token = os.getenv("BEARER_TOKEN")
openClient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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


def getPosts(keyword):
    # Fetch posts from both sources
    twitter_posts = fetch_twitter_posts(keyword, max_results=100)
    bluesky_posts = fetch_bluesky_posts(keyword, limit=100)

    # Combine results
    all_posts = twitter_posts + bluesky_posts

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
    
    print(f"Aggregate Sentiment Score: {aggregate_sentiment}")
    print(f"Total Posts Analyzed: {len(all_posts)}")
    
    return output_data

getPosts()



# def build_system_prompt(relevant_tweets):
#     """
#     Builds a system prompt containing the context of relevant tweets and their sentiment.
#     """
#     if not relevant_tweets:
#         context_text = "No tweets were found matching the query."
#     else:
#         context_text = "\n".join(
#             f"Tweet: {tweet['text']} (Sentiment: {tweet['sentiment']})"
#             for tweet in relevant_tweets
#         )
#     system_prompt = (
#         "You are a helpful assistant that answers questions based solely on a provided dataset of tweets "
#         "and their sentiment scores. Below is the dataset context:\n\n"
#         f"{context_text}\n\n"
#         "Answer the user's question using only the above information."
#     )
#     return system_prompt



@app.route('/api/chat', methods=['POST'])
def chat():
    # Make the session permanent (if desired)
    session.permanent = True

    # Initialize conversation history if it doesn't exist
    if 'messages' not in session:
        session['messages'] = [{"role": "system", "content": "This GPT, LSM Bot, is specialized in performing Linguistic Style Matching."}]

    user_input = request.json.get("query", "Just tell me if you are working fine please ")
    session['messages'].append({"role": "user", "content": user_input})
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=session['messages'],
            temperature=0.5,
            max_tokens=512,
        )
        response = completion.choices[0].message.content
        session['messages'].append({"role": "assistant", "content": response})
        return jsonify({"reply": response})
    except Exception as e:
        print("OpenAI API error:", e)
        return jsonify({"error": "Error communicating with OpenAI API"}), 500

if __name__ == '__main__':
    app.run(port=5000)
