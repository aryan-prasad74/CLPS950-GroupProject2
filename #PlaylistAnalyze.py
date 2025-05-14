import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

if os.path.exists(".cache"):
    os.remove(".cache")

#Spotify OAuth, authentication & login
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = "37c9bce1cdbc4583b26bd65253b04a36",
    client_secret = "4067ab6c82a1422289c534641e81d9c4",
    redirect_uri = "http://127.0.0.1:8888/callback",
    scope = "playlist-read-private user-top-read"
))

#List playlists
playlists = sp.current_user_playlists()
for idx, playlist in enumerate(playlists['items'], start = 1):
    print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

#Prompt user to select a playlist by index
selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
selected_playlist_id = playlists['items'][selected_index]['id']

#Get tracks of a selected playlist
tracks = sp.playlist_tracks(selected_playlist_id)

print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
cumulative_ids = []
for idx, item in enumerate (tracks['items'], start = 1):
    track = item['track']
    print(f"{idx}. {track['name']} (ID: {track['id']})")
    cumulative_ids.append(track['id'])
print(cumulative_ids)