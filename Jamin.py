import os
if os.path.exists(".cache"):
    os.remove(".cache")
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

# SpotifyOAuth handles token management automatically
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="95a3dd3dd0b241709a938b502eb7326a",
    client_secret="dc98f98db12d43149e4e6247a7a2fc08",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope= "playlist-read-private user-top-read"
))

# Get access token for direct HTTP calls
access_token = sp.auth_manager.get_access_token(as_dict=False)
headers = {"Authorization": f"Bearer {access_token}"}

def list_user_playlists():
    playlists = sp.current_user_playlists()
    for idx, playlist in enumerate(playlists['items'], start=1):
        print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")
    return playlists

def get_artist_ids_from_playlist(playlist_id):
    artist_ids = set()
    results = sp.playlist_tracks(playlist_id)
    
    # Paginate if needed
    while results:
        for item in results['items']:
            track = item['track']
            if track and track.get('artists'):
                for artist in track['artists']:
                    artist_ids.add(artist['id'])
        if results.get('next'):
            results = sp.next(results)
        else:
            results = None
    return list(artist_ids)

def get_recommendations(seed_artists, seed_genres, limit=20):
    base_url = "https://api.spotify.com/v1/recommendations"
    params = {
        "limit": limit,
        "seed_artists": ",".join(seed_artists[:5]),
        "seed_genres": ",".join(seed_genres[:5]) if seed_genres else ""
    }
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()

def create_playlist_with_recommendations(recommended_tracks, playlist_name="Generated from Playlist"):
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
    sp.playlist_add_items(playlist["id"], recommended_tracks)
    print(f"\n✅ Playlist '{playlist_name}' created with {len(recommended_tracks)} recommended tracks.")

def main():
    playlists = list_user_playlists()
    selected_index = int(input("\nEnter the index of the playlist to use as a seed: ")) - 1
    selected_playlist_id = playlists['items'][selected_index]['id']
    selected_playlist_name = playlists['items'][selected_index]['name']

    print(f"\n📥 Extracting artists from '{selected_playlist_name}'...")
    artist_ids = get_artist_ids_from_playlist(selected_playlist_id)
    print(f"Found {len(artist_ids)} unique artist(s).")

    genres_input = input("Enter comma-separated genres to include (or press Enter to skip): ").strip()
    seed_genres = [g.strip() for g in genres_input.split(',')] if genres_input else []

    print("\n🎯 Getting recommendations based on artists and genres...")
    recs = get_recommendations(artist_ids, seed_genres)
    track_ids = [track["id"] for track in recs.get("tracks", [])]

    create_playlist_with_recommendations(track_ids, playlist_name=f"Based on {selected_playlist_name}")

if __name__ == "__main__":
    main()