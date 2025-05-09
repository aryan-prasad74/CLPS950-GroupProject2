import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import xml.etree.ElementTree as ET

#Remove Existing cache file to ensure problem fresh authentication
if os.path.exists(".cache"):
    os.remove(".cache")

#Download and set up VADER lexicon - used for sentiment analysis
nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()


#Spotify OAuth authentication setup; User input credentials and redirect URI (TEST(G))
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = "95a3dd3dd0b241709a938b502eb7326a",
    client_secret = "dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri = "http://127.0.0.1:8888/callback",
    scope = "playlist-read-private user-top-read"
))

try:
    audio_features = sp.audio_features(tracks = ['2JzZzZUQj3Qff7wapcbKjc'])
    print(audio_features)
except SpotifyException as e:
    if e.http_status == 403:
        print("Access to the audio feautures endpoint is restricted for your application.")
    else: 
        print(f"An error occured: {e}")


#List user playlists
playlists = sp.current_user_playlists()
for idx, playlists in enumerate(playlists['items'], start = 1):
    print(f"{idx}, {playlists['name']} (ID: {playlists['id']})")

#Choose playlist
selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
selected_playlists_id = playlists['items'][selected_index]['id']

#Get tracks from selected playlist
tracks = sp.playlist_tracks(selected_playlists_id)
print(f"/nTracks in playlist '{playlists['items'][selected_index]['name']} ':")
cumulative_ids = []

#function to get lyrics using ChartLyrics API
def get_lyrics(track_name, artist_name):
    url = "http://api.chartlyrics.com/apivl.asmx/SearchLyricDirect"
    params = {"artist": artist_name, "song": track_name}
    try:
        response = requests.get(url, params = params, timeout = 5)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://api.chartlyrics.com/'}
        lyric = root.find('ns:Lyric', ns)
        if lyric is not None and lyric.text:
            print("Lyrics snippet:", lyric.text[:300])
            return lyric.text.strip()
        else:
            print("Lyrics not found.")
            return None
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None
    
#function to analyze lyric sentiment using VADER
def analyze_sentiment_vader(lyrics):
    if lyrics:
        scores = vader.polarity_scores(lyrics)
        compound = scores['compound']
        mood = "Positive" if compound > 0.3 else "Negative" if compound < -0.3 else "Neutreal"
        return mood, compound
    return "Unknown", 0.0

#Process each track
for idx, item in enumerate (tracks['items'], start = 1):
    track = item['track']
    name = track['name']
    artist = track['artists'][0]['name']
    print(f"\n{idx}. {name} by {artist}")

    cumulative_ids.append(track['id'])
    lyrics = get_lyrics(name, artist)
    if lyrics:
        mood, score = analyze_sentiment_vader(lyrics)
        print(f" Mood: {mood} (Compound Score: {score: .2f})")
    else:
        print("Lyrics not found")

print("\nTrack IDs collected:", cumulative_ids)
    
        


