#Login to Spotify → Choose Playlist → View Mood Profile → Generate Mood Playlist

import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Authentication details, identifies variables
client_id = "CLIENT ID"
client_secret = "CLIENT Secret"
redirect_uri = "http://localhost:8888/callback"
scope = "playlist-read-private playlist-read-collaborative user-library-read"


#Authenticate user
def authenticate_spotify_user():
    return spotipy.Spotify(auth_manager = SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_uri,
        scope = scope
    ))