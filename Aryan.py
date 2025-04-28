
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="a3596ff7cab74bbf870820453fc22d5e",
                                                           client_secret="589446335f0c4a29a3b894b364826006"))

results = sp.search(q='Drake', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

    print('hello')
