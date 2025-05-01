
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials and redirect URI --- TEST(G)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope= "playlist-read-private user-top-read"
))

######################## JSON Test ###############################
# import json
# response = sp.current_user_top_tracks(limit=10)
# print(json.dumps(response, indent=2))
##################################################################

## List playlists
playlists = sp.current_user_playlists()
for idx, playlist in enumerate(playlists['items'], start=1):
    print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

# Prompt the user to select a playlist by index
selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
selected_playlist_id = playlists['items'][selected_index]['id']

# Fetch the tracks in the selected playlist
tracks = sp.playlist_tracks(selected_playlist_id)

print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
cumulative_ids = []
for idx, item in enumerate(tracks['items'], start=1):
    track = item['track']
    print(f"{idx}. {track['name']} (ID: {track['id']})")
    cumulative_ids.append(track['id'])
print(cumulative_ids)


####################################### Find top artists #########################################
# top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')

# # Check if there are any top artists, if so display, else return msg.
# if top_artists['items']:
#     for idx, artist in enumerate(top_artists['items'], 1):
#         print(f"{idx}. {artist['name']}")
# else:
#     print("No top artists found.")

for i in range(0, len(cumulative_ids)):
    batch_ids = cumulative_ids[i:i+50]
    features = sp.audio_features(batch_ids)
    for feature in features:
        if feature:
            print(f"Track ID: {feature['id']}")
            print(f"  Energy: {feature['energy']}")
            print(f"  Tempo: {feature['tempo']}")
            print(f"  Valence: {feature['valence']}")
            print(f"  Danceability: {feature['danceability']}\n")