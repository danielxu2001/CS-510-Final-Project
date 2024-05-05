import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the value of MYANIMELIST_CLIENT_ID
client_id = os.getenv('MYANIMELIST_CLIENT_ID')
url = 'https://api.myanimelist.net/v2/anime'
params = {
    'q': 'one',
    'limit': 4
}
headers = {
    'X-MAL-CLIENT-ID': client_id
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    anime_data = response.json()
    print(anime_data)
else:
    print(f"Failed to retrieve anime data. Status code: {response.status_code}")
