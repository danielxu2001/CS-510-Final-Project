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
            status = entry['list_status']['status']
            title = entry['node']['title']
            anime_id = entry['node']['id']
            user_score = entry['list_status']['score']
            user_scores.append((username, anime_id, user_score, status, title))
        
        df = pd.DataFrame(user_scores, columns=["username", "anime_id", "my_score", "status", "title"])
        return df
    else:
        print(f"Failed to retrieve anime list. Status code: {response.status_code}")
        return None


def get_anime_data(anime_id):
    """
    Retrieves data for a specific anime by its ID from the MyAnimeList API.

    Args:
        anime_id (int): The ID of the anime.

    Returns:
        dict or None: A dictionary containing the data for the anime, or None if the request fails.
    """
    # Endpoint URL
    url = f'https://api.myanimelist.net/v2/anime/{anime_id}'
    # Query parameters
    params = {
        'fields': 'id,title,main_picture,synopsis,mean,num_scoring_users, genres'
    }
    # Headers
    headers = {
        'X-MAL-CLIENT-ID': client_id  # Assuming client_id is defined somewhere
    }

    # Make GET request to fetch anime data
    response = requests.get(url, params=params, headers=headers)
    # Check if request was successful
    if response.status_code == 200:
        anime_data = response.json()
        anime_id = anime_data['id']
        synopsis = anime_data['synopsis']
        title = anime_data['title']
        picture_url = anime_data['main_picture']['medium']
        score = anime_data['mean']
        num_scoring_user = anime_data['num_scoring_users']
        genres = ', '.join(genre['name'] for genre in anime_data.get('genres', []))
        # Add the anime data to a pandas series
        anime_detail = pd.Series({
            'anime_id': anime_id,
            'synopsis': synopsis,
            'title': title,
            'picture_url': picture_url,
            'score': score,
            'num_scoring_users': num_scoring_user,
            'genres': genres
        })

        
        return anime_detail
    else:
        print(f"Failed to retrieve anime data. Status code: {response.status_code}")
        return None

# # Example usage:
# anime_id = 30230  # Replace with the desired anime ID
# anime_data = get_anime_data(anime_id)
# print(anime_data)

def generate_html_table(anime_data_df):
    """
    Generates an HTML table from a list of anime data.

    Args:
        anime_data_df (pd.DataFrame): DataFrame containing anime data.

    Returns:
        str: HTML markup for the table.
    """
    table_html = """
    <table>
        <tr>
            <th>Image</th>
            <th>Title</th>
            <th>Genres</th>
            <th>Synopsis</th>
            <th>Score</th>
            <th>Number of Scored Users</th>
            <th>Estimated Rating</th>
        </tr>
    """


    for idx, anime_data in anime_data_df.iterrows():
        synopsis = anime_data['synopsis']
        title = anime_data['title']
        image_url = anime_data['picture_url']
        score = anime_data['score']
        num_scoring_user = anime_data['num_scoring_users']
        genres = anime_data['genres']
        estimated_rating = anime_data['estimated_rating']

        table_html += f"""
        <tr>
            <td><img src="{image_url}" alt="{title}" width="100"></td>
            <td>{title}</td>
            <td>{genres}</td>
            <td>{synopsis}</td>
            <td>{score}</td>
            <td>{f"{num_scoring_user:,}"}</td>
            <td>{round(estimated_rating, 2)}</td>
        </tr>
        """
        

    table_html += "</table>"
    return table_html

# Example usage:
# anime_data_list = get_anime_data(anime_id)
# if anime_data_list:
#     html_table = generate_html_table(anime_data_list)
#     print(html_table)
