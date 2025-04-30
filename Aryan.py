
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials and redirect URI --- TEST(G)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope= "playlist-read-private" #"user-top-read"
))

######################## JSON Test ###############################
# import json
# response = sp.current_user_top_tracks(limit=10)
# print(json.dumps(response, indent=2))
##################################################################

## List playlists
playlists = sp.current_user_playlists()
if playlists['items']:
    for idx, playlist in enumerate(playlists['items'], start=1):
        print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")
    else:
        print('No Playlists Found')


# #Find top artists
# top_artists = sp.current_user_top_artists(limit=1, time_range='short_term')

# # Check if there are any top artists, if so display, else return msg.
# if top_artists['items']:
#     for idx, artist in enumerate(top_artists['items'], 1):
#         print(f"{idx}. {artist['name']}")
# else:
#     print("No top artists found.")
#############################################################################################
