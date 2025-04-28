
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials and redirect URI
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="a3596ff7cab74bbf870820453fc22d5e",
    client_secret="589446335f0c4a29a3b894b364826006",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope=["user-top-read"]
))

# Fetch the current user's top artists
top_artists = sp.current_user_top_artists(limit=50, time_range='long_term')
print(top_artists)
# top_artist = top_artists['items'][0]
# print(f"Your top artist is {top_artist['name']}")
# if top_artists['items']:
#     top_artist = top_artists['items'][0]
#     print(f"Your top artist is {top_artist['name']}")
# else:
#     print("No top artist data available.")
