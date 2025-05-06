import os
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Remove .cache to reauthenticate
if os.path.exists(".cache"):
    os.remove(".cache")

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private user-top-read"
))

# Get user playlists
playlists = sp.current_user_playlists()
for idx, playlist in enumerate(playlists['items'], start=1):
    print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

# Select playlist
selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
selected_playlist_id = playlists['items'][selected_index]['id']

# Get tracks from playlist
tracks = sp.playlist_tracks(selected_playlist_id)
print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
cumulative_ids = []

def get_lyrics(track_name, artist_name):
    """Scrape lyrics from Genius."""
    query = f"{track_name} {artist_name} site:genius.com"
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for link in soup.select("a"):
        href = link.get("href")
        if "genius.com" in href:
            lyrics_url = href.split("&")[0].replace("/url?q=", "")
            lyrics_page = requests.get(lyrics_url, headers=headers)
            lyrics_soup = BeautifulSoup(lyrics_page.text, "html.parser")
            lyrics_div = lyrics_soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6")
            if lyrics_div:
                return lyrics_div.get_text(separator="\n")
    return None

def analyze_sentiment(lyrics):
    """Analyze sentiment using TextBlob."""
    if lyrics:
        blob = TextBlob(lyrics)
        polarity = blob.sentiment.polarity
        return polarity
    return None

# Process each track
for idx, item in enumerate(tracks['items'], start=1):
    track = item['track']
    name = track['name']
    artist = track['artists'][0]['name']
    print(f"\n{idx}. {name} by {artist}")
    
    cumulative_ids.append(track['id'])
    
    lyrics = get_lyrics(name, artist)
    if lyrics:
        sentiment = analyze_sentiment(lyrics)
        mood = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        print(f"  ➤ Mood: {mood} (Sentiment score: {sentiment:.2f})")
    else:
        print("  ➤ Lyrics not found.")

print("\nTrack IDs collected:", cumulative_ids)