
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your credentials and redirect URI --- TEST(G)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope= "playlist-read-private user-top-read"
))

print("Authenticated as:", sp.current_user()['display_name'])

# Track IDs
track_ids = [
    "3xdjjKMcMOFgo1eQrfbogM",
    "08er9ndoqL5gTp6eUdTTTw",
    "3fqwjXwUGN6vbzIwvyFMhx",
    "4obHzpwGrjoTuZh2DItEMZ"
]

# Get features
features = sp.audio_features(track_ids)
for f in features:
    if f:
        print(f"{f['id']}: danceability={f['danceability']}, energy={f['energy']}")
    else:
        print("No features available.")