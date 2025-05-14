
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials and redirect URI --- TEST(G)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    #client_id="95a3dd3dd0b241709a938b502eb7326a",
    #client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    client_id="a43a77e0821246f0a5cde04e9f6a35db",
    client_secret="0c1e99a30f0a4cc28b41220eaa8d0711",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope= "playlist-read-private user-top-read"
))



## List playlists
playlists = sp.current_user_playlists()
for idx, playlist in enumerate(playlists['items'], start=1):
    print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")


#Find top artists
top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')

# Check if there are any top artists, if so display, else return msg.
if top_artists['items']:
    for idx, artist in enumerate(top_artists['items'], 1):
        print(f"{idx}. {artist['name']}")
else:
    print("No top artists found.")
