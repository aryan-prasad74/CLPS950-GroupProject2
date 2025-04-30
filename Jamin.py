import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    
playlists = sp.current_user_playlists()
playlist_data = []

# Process each playlist
for playlist in playlists['items']:
    playlist_name = playlist['name']
    playlist_id = playlist['id']
    tracks = []
    results = sp.playlist_items(playlist_id)

    # Paginate through all tracks
    while results:
        tracks.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break

    # Get track IDs (excluding local and unavailable tracks)
    track_ids = [t['track']['id'] for t in tracks if t['track'] and t['track']['id']]
    audio_features = []

    # Fetch audio features in batches of 100
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        audio_features.extend(sp.audio_features(batch))

    # Filter out None values
    audio_features = [f for f in audio_features if f]

    if audio_features:
        # Compute average features
        avg_energy = sum(f['energy'] for f in audio_features) / len(audio_features)
        avg_valence = sum(f['valence'] for f in audio_features) / len(audio_features)
        avg_danceability = sum(f['danceability'] for f in audio_features) / len(audio_features)
        avg_tempo = sum(f['tempo'] for f in audio_features) / len(audio_features)

        mood = assign_mood(avg_valence, avg_energy)

        playlist_data.append({
            'Playlist Name': playlist_name,
            'Mood': mood,
            'Energy': avg_energy,
            'Tempo': avg_tempo,
            'Valence': avg_valence,
            'Danceability': avg_danceability
        })

# Create DataFrame
df = pd.DataFrame(playlist_data)