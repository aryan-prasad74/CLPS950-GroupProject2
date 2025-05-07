import os
if os.path.exists(".cache"):
    os.remove(".cache")
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import xml.etree.ElementTree as ET

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
    """Fetch lyrics from ChartLyrics API."""
    try:
        search_url = f"http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={requests.utils.quote(artist_name)}&song={requests.utils.quote(track_name)}"
        response = requests.get(search_url)
        if response.status_code != 200:
            print("  ➤ Failed to connect to ChartLyrics API.")
            return None

        soup = BeautifulSoup(response.text, 'xml')
        lyrics = soup.find('Lyric')
        if lyrics and lyrics.text.strip():
            print("Lyrics snippet:", lyrics.text.strip()[:300])
            return lyrics.text.strip()
        else:
            print("  ➤ No lyrics found on ChartLyrics.")
            return None

    except Exception as e:
        print(f"  ➤ Error fetching lyrics from ChartLyrics: {e}")
        return None

def analyze_sentiment_vader(lyrics):
    """Analyze sentiment using VADER."""
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