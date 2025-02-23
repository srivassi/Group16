import os
import requests
import json
from atproto import Client
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_session import Session
import openai
from datetime import timedelta
from flask_cors import CORS  

# Import external API functions
from twitter_API import fetch_twitter_posts
from bluesky_API import fetch_bluesky_posts

OpenAI = openai.OpenAI

# Load configuration from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow credentials with CORS

# Use a fixed secret key; ensure to set FLASK_SECRET_KEY in production
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load credentials for Twitter and OpenAI
api_key = os.getenv("API_KEY_TWITTER")
api_secret = os.getenv("API_SECRET_TWITTER")
bearer_token = os.getenv("BEARER_TOKEN")
openClient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def getPosts(keyword):
    """
    Fetch posts from Twitter and Bluesky APIs.
    Calculates aggregate sentiment and returns posts data.
    """
    # Fetch posts using external functions
    twitter_posts = fetch_twitter_posts(keyword, max_results=20)
    bluesky_posts = fetch_bluesky_posts(keyword, limit=20)

    # Combine posts and calculate aggregate sentiment
    all_posts = twitter_posts + bluesky_posts
    if all_posts:
        total_compound = sum(post["sentiment"]["compound"] for post in all_posts)
        avg_compound = total_compound / len(all_posts)
        aggregate_sentiment = ((avg_compound + 1) / 2) * 100  # Normalize to 0-100 scale
    else:
        aggregate_sentiment = None

    output_data = {
        "keyword": keyword,
        "aggregate_sentiment": aggregate_sentiment,
        "posts": all_posts
    }
    
    print(f"Aggregate Sentiment Score: {aggregate_sentiment}")
    print(f"Total Posts Analyzed: {len(all_posts)}")
    
    return output_data

def build_system_prompt(full_data):
    """
    Builds a system prompt with post data and sentiment scores.
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
    """
    Chat endpoint that processes user queries and sends a reply using OpenAI.
    """
    # Initialize conversation history if needed
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "This Bot has not yet received the required information. Please fetch posts first."}
        ]
    # Append system prompt if posts have been fetched and haven't been added yet
    elif 'posts' in session and not any("system prompt:" in msg.get("content", "") for msg in session['messages']):
        post_data = session.get('posts', None)
        sys_prompt = build_system_prompt(post_data)
        session['messages'].append({"role": "system", "content": f"system prompt: {sys_prompt}"})
    
    user_input = request.json.get("query", "Give me a summary of the data that you are working on")
    session['messages'].append({"role": "user", "content": user_input})
    
    try:
        # Call OpenAI API with the conversation history
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

@app.route('/api/getPosts', methods=['POST'])
def posts_route():
    """
    GET posts endpoint: Fetch posts from external APIs and store them in session.
    """
    data = request.json
    keyword = data.get("keyword", "Pope Francis")
    output_data = getPosts(keyword)
    # Ensure conversation history is initialized
    if 'messages' not in session:
        session['messages'] = []
    session['posts'] = output_data
    session['messages'].append({"role": "system", "content": f"Posts fetched for keyword: {keyword} are {output_data}"})
    return jsonify(output_data)

if __name__ == '__main__':
    app.run(port=5000)