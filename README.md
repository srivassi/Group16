# HackIreland Chat & Sentiment Analysis Bot

This project is a hackathon entry for [HackIreland](https://hackireland.com) that combines social media sentiment analysis with a conversational AI interface powered by OpenAI's GPT-3.5. The bot fetches posts from Twitter and Bluesky based on a user-specified keyword, processes the sentiment of each post, and provides a conversation context for ChatGPT to answer questions related to the dataset.

## Features

- **Social Media Data Retrieval:**  
  Fetches recent posts from Twitter and Bluesky using their APIs based on a provided keyword.

- **Sentiment Analysis:**  
  Uses the [VADER sentiment analysis](https://github.com/cjhutto/vaderSentiment) tool to compute sentiment scores for each post.

- **Conversational AI:**  
  Passes the aggregated social media data and sentiment context as a system prompt to ChatGPT, maintaining conversation history via Flask sessions.

- **Session Management:**  
  Uses Flask-Session to store conversation and fetched posts, ensuring continuity between user interactions.

## Prerequisites

- Python 3.8+
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Session](https://pythonhosted.org/Flask-Session/)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [atproto](https://github.com/bluesky-social/atproto) for Bluesky API integration
- Twitter API credentials
- Bluesky API credentials
- OpenAI API credentials

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/hackireland-chat-sentiment.git
   cd hackireland-chat-sentiment
