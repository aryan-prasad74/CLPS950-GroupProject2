
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# # Set your credentials and redirect URI --- TEST(G)
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id="95a3dd3dd0b241709a938b502eb7326a",
#     client_secret="dc98f98db12d43149e4e6247a7a2fc08",
#     redirect_uri="http://127.0.0.1:8888/callback",
#     scope= "playlist-read-private user-top-read"
# ))

# ######################## JSON Test ###############################
# # import json
# # response = sp.current_user_top_tracks(limit=10)
# # print(json.dumps(response, indent=2))
# ##################################################################

# ## List playlists
# playlists = sp.current_user_playlists()
# for idx, playlist in enumerate(playlists['items'], start=1):
#     print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

# # Select individual playlist by index
# selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
# selected_playlist_id = playlists['items'][selected_index]['id']

# # Fetch tracks in selected playlist
# tracks = sp.playlist_tracks(selected_playlist_id)

# #Print tracks and cumulative track ID list
# print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
# cumulative_ids = []
# for idx, item in enumerate(tracks['items'], start=1):
#     track = item['track']
#     print(f"{idx}. {track['name']} (ID: {track['id']})")
#     cumulative_ids.append(track['id'])
# print(cumulative_ids)


####################################### Find top artists #########################################
# top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')

# # Check if there are any top artists, if so display, else return msg.
# if top_artists['items']:
#     for idx, artist in enumerate(top_artists['items'], 1):
#         print(f"{idx}. {artist['name']}")
# else:
#     print("No top artists found.")





##############################################################################################################
##############################################################################################################

import os
if os.path.exists(".cache"):
    os.remove(".cache")
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException


# # Set your credentials and redirect URI --- TEST(G)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
     client_id="95a3dd3dd0b241709a938b502eb7326a",
     client_secret="dc98f98db12d43149e4e6247a7a2fc08",
     redirect_uri="http://127.0.0.1:8888/callback",
    scope= "playlist-read-private user-top-read"
 ))


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

#####################################################


try:
    audio_features = sp.audio_features(tracks=['2JzZzZUQj3Qff7wapcbKjc'])
    print(audio_features)
except SpotifyException as e:
    if e.http_status == 403:
        print("Access to the audio-features endpoint is restricted for your application.")
    else:
        print(f"An error occurred: {e}")

# print("\nAudio Features for each track:")
# for idx, features in enumerate(audio_features, start=1):
#     if features:  # Ensure the track's features were fetched successfully
#         print(f"{idx}. {features['id']}:")
#         print(f"   Danceability: {features['danceability']}")
#         print(f"   Energy: {features['energy']}")
#         print(f"   Valence: {features['valence']}")
#         print(f"   Tempo: {features['tempo']}")
#         print(f"   Acousticness: {features['acousticness']}")
#         print(f"   Instrumentalness: {features['instrumentalness']}")
#         print(f"   Liveness: {features['liveness']}")
#         print(f"   Speechiness: {features['speechiness']}")
#     else:
#         print(f"{idx}. No features available.")



#######################################################################################################################

import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import xml.etree.ElementTree as ET

# Remove existing cache
if os.path.exists(".cache"):
    os.remove(".cache")

# Download VADER lexicon if not already present
nltk.download('vader_lexicon')

# Setup VADER analyzer
vader = SentimentIntensityAnalyzer()

# Spotify OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private user-top-read"
))

# List user playlists
playlists = sp.current_user_playlists()
for idx, playlist in enumerate(playlists['items'], start=1):
    print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

# Choose playlist
selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
selected_playlist_id = playlists['items'][selected_index]['id']

# Get tracks
tracks = sp.playlist_tracks(selected_playlist_id)
print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
cumulative_ids = []

def get_lyrics(track_name, artist_name):
    """
    Fetch lyrics using the ChartLyrics API.
    """
    url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect"
    params = {"artist": artist_name, "song": track_name}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://api.chartlyrics.com/'}
        lyric = root.find('ns:Lyric', ns)
        if lyric is not None and lyric.text:
            print("Lyrics snippet:", lyric.text[:300])
            return lyric.text.strip()
        else:
            print("  ➤ Lyrics not found.")
            return None
    except Exception as e:
        print(f"  ➤ Error fetching lyrics: {e}")
        return None

def analyze_sentiment_vader(lyrics):
    """
    Analyze sentiment using VADER.
    """
    if lyrics:
        scores = vader.polarity_scores(lyrics)
        compound = scores['compound']
        mood = "Positive" if compound > 0.3 else "Negative" if compound < -0.3 else "Neutral"
        return mood, compound
    return "Unknown", 0.0

# Process each track
for idx, item in enumerate(tracks['items'], start=1):
    track = item['track']
    name = track['name']
    artist = track['artists'][0]['name']
    print(f"\n{idx}. {name} by {artist}")

    cumulative_ids.append(track['id'])
    lyrics = get_lyrics(name, artist)

    if lyrics:
        mood, score = analyze_sentiment_vader(lyrics)
        print(f"  ➤ Mood: {mood} (Compound Score: {score:.2f})")
    else:
        print("  ➤ Lyrics not found.")

print("\nTrack IDs collected:", cumulative_ids)
