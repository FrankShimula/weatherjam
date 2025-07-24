import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
load_dotenv()


def spotify_auth():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-modify-playback-state user-read-playback-state user-read-currently-playing"
    ))

def mood_to_query(mood):
    queries = {
        "chill": "chill vibes",
        "lo-fi": "lofi hip hop",
        "acoustic": "acoustic chill",
        "indie": "indie pop",
        "pop": "today's top hits",
        "summer vibes": "summer hits",
        "ambient": "ambient music",
        "cinematic": "epic soundtrack"
    }
    return queries.get(mood, mood)


def check_devices(sp):
    """Check available Spotify devices"""
    try:
        devices = sp.devices()
        print(f"\nAvailable devices ({len(devices['devices'])}):")
        
        active_device = None
        for i, device in enumerate(devices['devices']):
            status = "🟢 ACTIVE" if device['is_active'] else "⚪ inactive"
            print(f"  {i+1}. {device['name']} ({device['type']}) - {status}")
            if device['is_active']:
                active_device = device
                
        return devices['devices'], active_device
    except Exception as e:
        print(f"Error checking devices: {e}")
        return [], None


def check_premium_status(sp):
    """Check if user has premium by trying to get current playback"""
    try:
        current = sp.current_playback()
        user = sp.current_user()
        print(f"User: {user['display_name']}")
        print(f"Subscription: {user.get('product', 'unknown')}")
        return user.get('product') == 'premium'
    except Exception as e:
        print(f"Error checking premium status: {e}")
        return False


def play_mood_music(sp, mood):
    query = mood_to_query(mood)
    
    try:
        # Check premium status
        print("Checking Spotify account status...")
        is_premium = check_premium_status(sp)
        if not is_premium:
            print("❌ Premium subscription required for playback control")
            return False
            
        # Check available devices
        devices, active_device = check_devices(sp)
        
        if not devices:
            print("❌ No Spotify devices found. Please open Spotify on a device first.")
            return False
            
        if not active_device:
            print("❌ No active device found. Please start playing something on Spotify first, then try again.")
            print("💡 Tip: Open Spotify and play any song, then pause it. This will make the device 'active'.")
            return False
            
        print(f"✅ Using device: {active_device['name']}")
        
        # Search for playlists
        results = sp.search(q=query, type='playlist', limit=10)
        print(f"Searching for: '{query}'")
        print(f"Total playlists found: {results['playlists']['total']}")
        
        items = results['playlists']['items']
        valid_playlists = [item for item in items if item is not None]
        
        if not valid_playlists:
            print(f"No valid playlists found for '{query}', trying fallback...")
            fallback_queries = ["chill music", "popular music", "top hits"]
            for fallback in fallback_queries:
                results = sp.search(q=fallback, type='playlist', limit=10)
                items = results['playlists']['items']
                valid_playlists = [item for item in items if item is not None]
                if valid_playlists:
                    print(f"Found playlist with fallback: '{fallback}'")
                    break
        
        if not valid_playlists:
            print("❌ No playlists found")
            return False
            
        # Use the first valid playlist
        playlist = valid_playlists[0]
        uri = playlist.get('uri')
        name = playlist.get('name', 'Unknown')
        
        print(f"🎵 Playing: '{name}'")
        
        # Try to start playback
        sp.start_playback(context_uri=uri, device_id=active_device['id'])
        print(f"✅ Successfully started playback for mood: {mood}")
        return True
        
    except spotipy.exceptions.SpotifyException as e:
        error_msg = str(e)
        print(f"❌ Spotify API error: {e}")
        
        if "PREMIUM_REQUIRED" in error_msg:
            print("🔄 Premium required error. Try these steps:")
            print("   1. Log out of Spotify completely")
            print("   2. Log back in at spotify.com")
            print("   3. Verify your subscription at spotify.com/account")
            print("   4. Delete .cache file and re-authenticate")
            
        elif "NO_ACTIVE_DEVICE" in error_msg:
            print("🔄 Try opening Spotify and playing any song first")
            
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def alternative_playback(sp, mood):
    """Alternative approach - just add songs to queue instead of controlling playback"""
    try:
        query = mood_to_query(mood)
        
        # Search for tracks instead of playlists
        results = sp.search(q=query, type='track', limit=5)
        tracks = results['tracks']['items']
        
        if not tracks:
            print("No tracks found")
            return False
            
        print(f"Adding {len(tracks)} songs to your queue:")
        for track in tracks:
            sp.add_to_queue(track['uri'])
            print(f"  + {track['name']} by {track['artists'][0]['name']}")
            
        print("✅ Songs added to queue! Press next in Spotify to hear them.")
        return True
        
    except Exception as e:
        print(f"Queue approach failed: {e}")
        return False