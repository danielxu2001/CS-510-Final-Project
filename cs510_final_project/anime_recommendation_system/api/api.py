import requests
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get the value of MYANIMELIST_CLIENT_ID
client_id = os.getenv('MYANIMELIST_CLIENT_ID')
url = 'https://api.myanimelist.net/v2/anime'
params = {
    'q': 'one',
    'limit': 100  # Set the limit per page to the maximum allowed by the API
}
headers = {
    'X-MAL-CLIENT-ID': client_id
}


def get_user_anime_list(username):
    """
    Retrieves the anime list of the specified user from MyAnimeList API.

    Args:
        username (str): The username of the user.

    Returns:
        list of tuples: A list of tuples containing (username, anime_id, user_score) for each entry in the anime list, 
                        or None if the request fails.
    """
    # Endpoint URL
    url = f'https://api.myanimelist.net/v2/users/{username}/animelist'
    # Query parameters
    params = {
        'fields': 'list_status',
        'limit': 1000
    }
    # Headers
    headers = {
        'X-MAL-CLIENT-ID': client_id  # Assuming client_id is defined somewhere
    }

    # Make GET request to fetch anime list
    response = requests.get(url, params=params, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        anime_list = response.json()
        user_scores = []
        for entry in anime_list['data']:
            anime_id = entry['node']['id']
            user_score = entry['list_status']['score']
            user_scores.append((username, anime_id, user_score))
        
        df = pd.DataFrame(user_scores, columns=["username", "anime_id", "my_score"])
        return df
    else:
        print(f"Failed to retrieve anime list. Status code: {response.status_code}")
        return None

# # Example usage:
# username = 'relight'
# anime_scores = get_user_anime_list(username)
# if anime_scores:
#     for username, anime_id, user_score in anime_scores:
#         print("Username: {}, Anime ID: {}, Score: {}".format(username, anime_id, user_score))
