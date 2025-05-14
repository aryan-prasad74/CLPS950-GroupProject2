# import os
# if os.path.exists(".cache"):
#     os.remove(".cache")
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# # Spotify OAuth
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id="37c9bce1cdbc4583b26bd65253b04a36",
#     client_secret="4067ab6c82a1422289c534641e81d9c4",
#     redirect_uri="http://127.0.0.1:8888/callback",
#     scope="playlist-read-private user-top-read"
# ))


# ## List playlists
# playlists = sp.current_user_playlists()
# for idx, playlist in enumerate(playlists['items'], start=1):
#     print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

# # Prompt the user to select a playlist by index
# selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
# selected_playlist_id = playlists['items'][selected_index]['id']

# # Fetch the tracks in the selected playlist
# tracks = sp.playlist_tracks(selected_playlist_id)

# print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
# cumulative_ids = []
# for idx, item in enumerate(tracks['items'], start=1):
#     track = item['track']
#     print(f"{idx}. {track['name']} (ID: {track['id']})")
#     cumulative_ids.append(track['id'])
# print(cumulative_ids)


# audio_features = sp.audio_features(cumulative_ids)

# print("\nAudio Features for each track:")
# for idx, features in enumerate(audio_features, start=1):
#     if features:  # Ensure the track's features were fetched successfully
#         print(f"{idx}. {features['id']}:")
#         print(f"   Danceability: {features['danceability']}")
#         print(f"   Energy: {features['energy']}")
#         print(f"   Valence: {features['valence']}")
#         print(f"   Tempo: {features['tempo']}")
#     else:
#         print(f"{idx}. No features available.")