import os
import requests
import json
from atproto import Client
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify, session
from flask_session import Session
import openai
from datetime import timedelta
from flask_cors import CORS  # new import

OpenAI = openai.OpenAI

# Load environment variables from .env or your IDE configuration.
load_dotenv()

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Updated to allow credentials in CORS
# Use a fixed secret key from the environment or default (ensure to set FLASK_SECRET_KEY in production)
app.secret_key = app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"  # You can use 'redis' or another backend as needed.
# app.config["SESSION_PERMANENT"] = True
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)

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
def fetch_twitter_posts(keyword, max_results=30):
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

def fetch_bluesky_posts(keyword, limit=30):
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
    twitter_posts = fetch_twitter_posts(keyword, max_results=20)
    bluesky_posts = fetch_bluesky_posts(keyword, limit=20)

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

    # Remove sentiment from each post for final JSON output
    # filtered_posts = [{"source": post["source"], "text": post["text"]} for post in all_posts]

    # output_data = {
    #     "keyword": keyword,
    #     "aggregate_sentiment": aggregate_sentiment,
    #     "posts": filtered_posts
    # }
    
    # print(f"Aggregate Sentiment Score: {aggregate_sentiment}")
    # print(f"Total Posts Analyzed: {len(all_posts)}")
    
    # return output_data


def build_system_prompt(full_data):
    """
    Builds a system prompt containing the context of posts and their sentiment.
    """
    posts = full_data.get("posts", []) if full_data else []
    if not posts:
        context_text = "No posts were found for the provided keyword."
    else:
        context_text = "\n".join(
            f"{post['source']} Post: {post['text']} (Sentiment: {post['sentiment']})"
            for post in posts
        )
    system_prompt = (
        "You are a helpful assistant that answers questions based solely on a provided dataset of posts "
        "and their sentiment scores. Below is the dataset context:\n\n"
        f"{context_text}\n\n"
        "You first generate a future plan of action on how the aggregate sentiment score can be improved and/or maintained. "
        "Answer the user's question using the above information."
    )
    return system_prompt


@app.route('/api/chat', methods=['POST'])
def chat():

    # Initialize conversation history if it doesn't exist
    
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "This Bot has not yet received the required information. Please fetch posts first."}
        ]
    # Only append system prompt from posts once if it's not already there.
    elif 'posts' in session and not any("system prompt:" in msg.get("content", "") for msg in session['messages']):
        post_data = session.get('posts', None)
        sys_prompt = build_system_prompt(post_data)
        session['messages'].append({"role": "system", "content": f"system prompt: {sys_prompt}"})
    

    user_input = request.json.get("query", "Give me a summary of the data that you are working on")
    session['messages'].append({"role": "user", "content": user_input})
    
    try:
        completion = openClient.chat.completions.create(
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

# New POST route to call getPosts(), store results in session, and return output data.
@app.route('/api/getPosts', methods=['POST'])
def posts_route():
    data = request.json
    keyword = data.get("keyword", "Pope Francis")
    output_data = getPosts(keyword)
    # Ensure session['messages'] is initialized
    if 'messages' not in session:
        session['messages'] = []
    session['posts'] = output_data
    session['messages'].append({"role": "system", "content": f"Posts fetched for keyword: {keyword} are {output_data}"})
    return jsonify(output_data)

if __name__ == '__main__':
    app.run(port=5000)