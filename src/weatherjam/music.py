import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()


def spotify_auth():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-modify-playback-state user-read-playback-state"
    ))

def play_mood_music(sp, mood):
    results = sp.search(q=mood, type='playlist', limit=1)
    playlist = results['playlists']['items'][0]
    sp.start_playback(context_uri=playlist['uri'])
