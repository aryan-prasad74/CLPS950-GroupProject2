import os
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import xml.etree.ElementTree as ET


def profile_track_analysis():

    #remove existing cache
    if os.path.exists(".cache"):
        os.remove(".cache")

    #download VADER lexicon if not already present
    nltk.download('vader_lexicon')

    #setup VADER analyzer
    vader = SentimentIntensityAnalyzer()

    #Spotify OAuth, authentication & login
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = "37c9bce1cdbc4583b26bd65253b04a36",
    client_secret = "4067ab6c82a1422289c534641e81d9c4",
    redirect_uri = "http://127.0.0.1:8888/callback",
    scope = "playlist-read-private user-top-read"
    ))

    def get_lyrics(track_name, artist_name):
        url = "http://api.chartlyrics.com/apivl.asmx/SearchLyricsDirect"
        params = {"artist": artist_name, "song": track_name}
        try:
            response = requests.get(url, params = params, timeout = 5)
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
    
    #Retrieve all user playlists
    playlists = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit = 50, offset = offset)
        playlists.extend(response['items'])
        if response['next']:
            offset += 50
        else:
            break

    print(f"Total playlist found: {len(playlists)}")

    #Initialize counters and lists
    total_tracks = 0
    tracks_with_lyrics = 0
    analyzed_tracks = []
    compound_scores = []

        #process each playlist
    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        print(f"\nProcessing playlist: {playlist_name}")

        #retrieve all tracks in playlist
        tracks = []
        offset = 0
        while True:
            response = sp.playlist_tracks(playlist_id, limit = 100, offset = offset)
            tracks.extend(response['items'])
            if response ['next']:
                offset += 100
            else:
                break

        print(f" Total tracks in playlist: {len(tracks)}") 

        for item in tracks:
            track = item['track']
            if track is None:
                continue
            name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            artist_name = ', '.join(artists)
            total_tracks += 1

            lyrics = get_lyrics(name, artist_name)
            if lyrics:
                mood, score = analyze_sentiment_vader(lyrics)
                tracks_with_lyrics += 1
                analyzed_tracks.append(f"{name} by {artist_name}")
                compound_scores.append(score)
                print(f" Analyzed: {name} by {artist_name}; Mood: {mood} (Score: {score:.2f})") 
            else:
                print(f" Skipped (lyrics not found): {name} by {artist_name}")   

    #Summary
    print("\n\nAnalysis Summary:")   
    print(f" Total tracks processed: {total_tracks}")
    print(f" Tracks with lyrics found: {tracks_with_lyrics}")  
    if total_tracks > 0:
        print(f" Success rate: {tracks_with_lyrics}/{total_tracks} ({(tracks_with_lyrics/total_tracks)*100:.2f}%)")
    else:
        print("No tracks processed.")

    #output lists
    print("\nTracks successfully analyzed:")
    for track in analyzed_tracks:
        print(f"{track}")

    print("\nCorresponding compound sentiment scores:")
    for score in compound_scores:
        print(f"{score: .2f}")

    print(analyzed_tracks) #list of indexed tracks
    print(compound_scores) #list of indexed scores
    return analyzed_tracks, compound_scores
        
analyzed_tracks, compound_scores = profile_track_analysis()