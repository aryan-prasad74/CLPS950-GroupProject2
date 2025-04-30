import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private playlist-read-collaborative"
))

def assign_mood(valence, energy):
    if valence >= 0.6 and energy >= 0.6:
        return "Happy"
    elif valence >= 0.6 and energy < 0.6:
        return "Chill"
    elif valence < 0.4 and energy < 0.5:
        return "Sad"
    elif valence < 0.5 and energy >= 0.6:
        return "Angsty"
    else:
        return "Calm"