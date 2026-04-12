import os
import requests
from dotenv import load_dotenv  # Parse a .env file and load variables as environment variables

# Loading environment variables from a .env file
load_dotenv()

# Retrieving the DEV API key from environment variables
DEV_API_KEY = os.getenv("DEV_API_KEY")

# Endpoint to fetch the authenticated user's articles from dev.to
DEV_API_URL = "https://dev.to/api/articles/me"

def fetchMyArticles():
    """
    Fetch all articles of the authenticated user from dev.to. This function makes a request to the dev.to API using the provided API key,
    retrieves the user's articles, and extracts only the required fields such as title, URL, cover image, markdown content, and tags.

    Returns:
        list: A list of dictionaries containing cleaned article data. Returns an empty list if the request fails.
    """
    
    # Fetching articles from dev.to
    print("Fetching articles from dev.to...")
    
    # Setting up request headers with API key and required format
    headers = {
        "api-key": DEV_API_KEY,
        "Accept": "application/vnd.forem.api-v1+json"
    }
    
    # Sending GET request to dev.to API
    response = requests.get(DEV_API_URL, headers=headers)
    
    # Handling case - request failed
    if response.status_code != 200:
        print(f"Failed to fetch articles (status code: {response.status_code})")
        return []
    
    # Parsing response JSON data
    articles = response.json()
    
    # Logging number of articles fetched
    print(f"Fetched {len(articles)} articles.")
    
    # Extracting only the required fields from each article
    extracted_data = []
    for article in articles:
        extracted_data.append(
            {
                "title": article.get("title"),
                "url": article.get("url"),
                "cover_image": article.get("cover_image"),
                "body_markdown": article.get("body_markdown"),
                "tags": article.get("tag_list", [])
            }
        )
    
    # Returning cleaned article data
    return extracted_data