import os
if os.path.exists(".cache"):
    os.remove(".cache")
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

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
    query = f"{track_name} {artist_name} site:genius.com"
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")  # Suppress logs

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)
    time.sleep(2)

    # Find first Genius link
    links = driver.find_elements("tag name", "a")
    genius_url = None
    for link in links:
        href = link.get_attribute("href")
        if href and "genius.com" in href:
            genius_url = href
            break

    if not genius_url:
        driver.quit()
        return None

    # Visit Genius page
    driver.get(genius_url)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    lyrics_divs = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-6")

    driver.quit()

    if lyrics_divs:
        return "\n".join([div.get_text(separator="\n") for div in lyrics_divs])
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