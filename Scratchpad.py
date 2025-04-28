import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials and redirect URI --- TEST 2
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="3bd1abd2ffd2463a8a86a7bf77b6e113",
    client_secret="0f365761c29d4fe5a595b0dd4814dfe9",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope=["user-top-read"]
))
print(sp.auth_manager.get_cached_token())
print(sp.current_user())  

# Fetch the current user's top artists
top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
print(top_artists)

## Rest of top artist display code ##
# top_artist = top_artists['items'][0]
# print(f"Your top artist is {top_artist['name']}")
# if top_artists['items']:
#     top_artist = top_artists['items'][0]
#     print(f"Your top artist is {top_artist['name']}")
# else:
#     print("No top artist data available.")

## To Test for 200 OK code ##
    # import requests
    # headers = {"Authorization": "Bearer " + sp.auth_manager.get_cached_token()['access_token']}
    # r = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=headers)
    # print(r.status_code, r.json())

    