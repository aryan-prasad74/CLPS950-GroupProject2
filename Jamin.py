import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import xml.etree.ElementTree as ET

def get_lyrics(track_name, artist_name):
    url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect"
    params = {"artist": artist_name, "song": track_name}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://api.chartlyrics.com/'}
        lyric = root.find('ns:Lyric', ns)
        return lyric.text.strip() if lyric is not None and lyric.text else None
    except Exception:
        return None

def analyze_sentiment(lyrics, vader):
    if lyrics:
        score = vader.polarity_scores(lyrics)['compound']
        return score
    return None

def profile_track_analysis(mood_tolerance=0.05):
    # Download VADER lexicon if not already present
    nltk.download('vader_lexicon', quiet=True)
    vader = SentimentIntensityAnalyzer()

    # Remove existing Spotify cache
    if os.path.exists(".cache"):
        os.remove(".cache")

    # Spotify OAuth setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
       client_id="37c9bce1cdbc4583b26bd65253b04a36",
       client_secret="4067ab6c82a1422289c534641e81d9c4",
       redirect_uri="http://127.0.0.1:8888/callback",
       scope="playlist-read-private user-top-read playlist-modify-private"
   ))


    # Collect user playlists
    playlists = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=50, offset=offset)
        playlists.extend(response['items'])
        if response['next']:
            offset += 50
        else:
            break

    print(f"\nFound {len(playlists)} playlists.")
    total_tracks = 0
    track_scores = {}

    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        print(f"\nAnalyzing playlist: {playlist_name}")
        tracks = []
        offset = 0
        while True:
            response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
            tracks.extend(response['items'])
            if response['next']:
                offset += 100
            else:
                break

        for item in tracks:
            track = item['track']
            if not track or not track.get('id'):
                continue
            track_name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            artist_name = ', '.join(artists)
            track_uri = track['uri']
            total_tracks += 1

            if track_uri not in track_scores:  # Avoid duplicates
                lyrics = get_lyrics(track_name, artist_name)
                if lyrics:
                    score = analyze_sentiment(lyrics, vader)
                    if score is not None:
                        track_scores[track_uri] = (f"{track_name} by {artist_name}", score)
                        print(f"{track_name} by {artist_name} Score: {score:.2f}")
                    else:
                        print(f"Sentiment failed: {track_name} by {artist_name}")
                else:
                    print(f"Lyrics not found: {track_name} by {artist_name}")

    print(f"\nProcessed {total_tracks} tracks.")
    print(f"Tracks with sentiment scores: {len(track_scores)}")

    user_id = sp.current_user()['id']

    # Loop for repeated mood input
    while True:
        try:
            mood_index = float(input("\nEnter desired mood index (-1 to 1), or 'q' to quit: "))
        except ValueError:
            print("Exiting.")
            break

        if not -1.0 <= mood_index <= 1.0:
            print("Mood index must be between -1 and 1.")
            continue

        # Filter by mood score
        def filter_tracks_by_tolerance(tolerance):
            return [
                uri for uri, (_, score) in track_scores.items()
                if abs(score - mood_index) <= tolerance
            ]

        tolerances = [mood_tolerance, 0.1, 0.15]
        matching_tracks = []

        for tol in tolerances:
            matching_tracks = filter_tracks_by_tolerance(tol)
            if len(matching_tracks) >= 10:
                print(f"\nFound {len(matching_tracks)} tracks within ±{tol:.2f} of {mood_index:.2f}.")
                break
            else:
                print(f"\nOnly {len(matching_tracks)} tracks found within ±{tol:.2f}. Trying wider range...")

        if len(matching_tracks) < 10:
            print(f"\nStill only {len(matching_tracks)} tracks found. Proceeding with available tracks.")

        # Create playlist
        if matching_tracks:
            playlist_title = f"Mood Playlist ({mood_index:+.2f})"
            new_playlist = sp.user_playlist_create(
                user=user_id,
                name=playlist_title,
                public=False,
                description=f"Songs with mood around {mood_index:+.2f}"
            )
            sp.playlist_add_items(new_playlist['id'], matching_tracks[:100])
            print(f"Created playlist: {playlist_title}")
        else:
            print("No songs matched the mood range. Playlist not created.")

# Run
profile_track_analysis()