from dotenv import load_dotenv
from weatherjam.weather import get_weather, weather_to_mood, get_location
from weatherjam.music import spotify_auth, play_mood_music, alternative_playback

def main():
    load_dotenv()

    # Get location and weather
    location = get_location()
    if not location:
        print("❌ Could not get location")
        return
        
    print(f"📍 Location: {location['city']}, {location['country']}")

    weather = get_weather()
    if not weather:
        print("❌ Could not get weather data")
        return
        
    mood = weather_to_mood(weather)
    print(f"🌤️  Weather: {weather}, Mood: {mood}")

    # Try Spotify authentication
    try:
        sp = spotify_auth()
        print("✅ Spotify authentication successful")
    except Exception as e:
        print(f"❌ Spotify authentication failed: {e}")
        print("Check your SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")
        return

    # Try main playback approach
    print("\n🎵 Attempting to play mood music...")
    success = play_mood_music(sp, mood)
    
    # If main approach fails, try alternative
    if not success:
        print("\n🔄 Trying alternative approach (adding to queue)...")
        alternative_success = alternative_playback(sp, mood)
        
        if not alternative_success:
            print("\n💡 Manual steps:")
            print("1. Open Spotify and play any song")
            print("2. Run this script again")
            print("3. Or manually search for playlists matching your mood:", mood)

if __name__ == "__main__":
    main()