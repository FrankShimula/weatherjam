from weatherjam.weather import get_weather, weather_to_mood
from weatherjam.music import spotify_auth, play_mood_music

def main():
    lat = 52.37    # change this
    lon = 4.89

    weather = get_weather(lat, lon)
    mood = weather_to_mood(weather)
    print(f"Weather: {weather}, Mood: {mood}")

    sp = spotify_auth()
    play_mood_music(sp, mood)

if __name__ == "__main__":
    main()
