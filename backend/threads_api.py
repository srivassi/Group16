import requests


def get_data_from_threads(api_endpoint, token):
    """
    Performs a GET request to the specified Threads API endpoint.

    :param api_endpoint: URL of the API endpoint.
    :param token: Your API access token.
    :return: Parsed JSON response if successful, None otherwise.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print("GET request failed:", e)
        return None


def post_data_to_threads(api_endpoint, token, payload):
    """
    Performs a POST request to the specified Threads API endpoint with given payload.

    :param api_endpoint: URL of the API endpoint.
    :param token: Your API access token.
    :param payload: A dictionary with the data to send.
    :return: Parsed JSON response if successful, None otherwise.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print("POST request failed:", e)
        return None


def main():
    # Replace these with your actual Threads API details
    token = "YOUR_ACCESS_TOKEN"  # Your API token
    get_endpoint = "https://api.threads.net/your-get-endpoint"  # GET endpoint URL
    post_endpoint = "https://api.threads.net/your-post-endpoint"  # POST endpoint URL

    # Example: Making a GET request
    print("Performing GET request...")
    get_response = get_data_from_threads(get_endpoint, token)
    if get_response is not None:
        print("GET response:", get_response)
    else:
        print("Failed to retrieve data from the GET endpoint.")

    # Example: Making a POST request
    print("\nPerforming POST request...")
    payload = {
        "message": "Hello, Threads!",
        "user_id": "123456"
    }
    post_response = post_data_to_threads(post_endpoint, token, payload)
    if post_response is not None:
        print("POST response:", post_response)
    else:
        print("Failed to post data to the API.")


if __name__ == "__main__":
    main()
