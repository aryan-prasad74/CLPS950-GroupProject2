import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import xml.etree.ElementTree as ET

def profile_track_analysis(mood_selection_input=0.5, mood_tolerance=0.05):
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
        scope="playlist-read-private playlist-modify-public playlist-modify-private user-top-read"
    ))

    def get_lyrics(track_name, artist_name):
        url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect"
        params = {"artist": artist_name, "song": track_name}
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            ns = {'ns': 'http://api.chartlyrics.com/'}
            lyric = root.find('ns:Lyric', ns)
            if lyric is not None and lyric.text:
                return lyric.text.strip()
            else:
                return None
        except Exception:
            return None

    def analyze_sentiment_vader(lyrics):
        if lyrics:
            scores = vader.polarity_scores(lyrics)
            compound = scores['compound']
            mood = "Positive" if compound > 0.3 else "Negative" if compound < -0.3 else "Neutral"
            return mood, compound
        return "Unknown", 0.0

    # Retrieve all user playlists
    playlists = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=50, offset=offset)
        playlists.extend(response['items'])
        if response['next']:
            offset += 50
        else:
            break

    print(f"Total playlists found: {len(playlists)}")

    # Initialize counters and lists
    total_tracks = 0
    tracks_with_lyrics = 0
    track_score_map = {}  # Track URI ➤ compound score

    # Process each playlist
    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        print(f"\nProcessing playlist: {playlist_name}")

        # Retrieve all tracks in the playlist
        tracks = []
        offset = 0
        while True:
            response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
            tracks.extend(response['items'])
            if response['next']:
                offset += 100
            else:
                break

        print(f"  Total tracks in playlist: {len(tracks)}")

        for item in tracks:
            track = item['track']
            if not track or not track.get('id'):
                continue
            name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            artist_name = ', '.join([artist for artist in artists if artist])
            track_uri = track['uri']
            total_tracks += 1

            lyrics = get_lyrics(name, artist_name)
            if lyrics:
                mood, score = analyze_sentiment_vader(lyrics)
                tracks_with_lyrics += 1
                track_score_map[track_uri] = (f"{name} by {artist_name}", score)
                print(f"    Analyzed: {name} by {artist_name} ➤ Mood: {mood} (Score: {score:.2f})")
            else:
                print(f"    Skipped (lyrics not found): {name} by {artist_name}")

    # Summary
    print("\n\nAnalysis Summary:")
    print(f"  Total tracks processed: {total_tracks}")
    print(f"  Tracks with lyrics found: {tracks_with_lyrics}")
    if total_tracks > 0:
        print(f"  Success rate: {tracks_with_lyrics}/{total_tracks} ({(tracks_with_lyrics/total_tracks)*100:.2f}%)")
    else:
        print("  No tracks processed.")

    # Filter by mood score
    selected_tracks = [
        uri for uri, (_, score) in track_score_map.items()
        if abs(score - mood_selection_input) <= mood_tolerance
    ]

    print(f"\nSelected {len(selected_tracks)} tracks within ±{mood_tolerance:.2f} of mood score {mood_selection_input:.2f}.")

    # Create new playlist
    if selected_tracks:
        user_id = sp.current_user()['id']
        playlist_name = f"Custom Mood Playlist ({mood_selection_input:.2f})"
        new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description="Auto-generated mood playlist")
        sp.playlist_add_items(new_playlist['id'], selected_tracks[:100])  # Limit to 100 for simplicity
        print(f"Created playlist: {playlist_name}")
    else:
        print("No tracks matched the mood criteria. Playlist not created.")

    return track_score_map

# Example run with mood score around 0.5 (somewhat positive)
track_score_map = profile_track_analysis(mood_selection_input=0.5, mood_tolerance=0.05)