import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_weather(lat, lon):
    key = os.getenv("TOMORROW_API_KEY")
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={key}"
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # Raises an HTTPError for bad responses
        data = res.json()
        
        if 'data' not in data or 'values' not in data['data']:
            print(f"Unexpected API response format: {data}")
            return None
            
        values = data["data"]["values"]
        return {
            "condition": str(values["weatherCode"]),
            "temp": values["temperature"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Weather API request failed: {e}")
        return None
    except KeyError as e:
        print(f"Missing expected field in weather data: {e}")
        return None


def get_location():
    try:
        res = requests.get("http://ip-api.com/json/", timeout=10)
        res.raise_for_status()
        data = res.json()
        
        return {
            "lat": data["lat"],
            "lon": data["lon"],
            "city": data["city"],
            "country": data["country"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Location API request failed: {e}")
        return None


def weather_to_mood(weather):
    if weather is None:
        return "chill"  # Default fallback
        
    code = weather["condition"]
    temp = weather["temp"]
    
    # Tomorrow.io weather codes mapping
    weather_code_map = {
        # Clear/Sunny
        "1000": "pop",      # Clear, Sunny
        "1100": "pop",      # Mostly Clear
        "1101": "indie",    # Partly Cloudy
        "1102": "indie",    # Mostly Cloudy
        "1001": "indie",    # Cloudy
        
        # Fog
        "2000": "ambient",  # Fog
        "2100": "ambient",  # Light Fog
        
        # Drizzle
        "4000": "lo-fi",    # Drizzle
        "4001": "lo-fi",    # Rain
        "4200": "lo-fi",    # Light Rain
        "4201": "lo-fi",    # Heavy Rain
        
        # Snow
        "5000": "acoustic", # Snow
        "5001": "acoustic", # Flurries
        "5100": "acoustic", # Light Snow
        "5101": "acoustic", # Heavy Snow
        
        # Freezing Rain
        "6000": "acoustic", # Freezing Drizzle
        "6001": "acoustic", # Freezing Rain
        "6200": "acoustic", # Light Freezing Rain
        "6201": "acoustic", # Heavy Freezing Rain
        
        # Ice Pellets
        "7000": "ambient",  # Ice Pellets
        "7101": "ambient",  # Heavy Ice Pellets
        "7102": "ambient",  # Light Ice Pellets
        
        # Thunderstorm
        "8000": "cinematic", # Thunderstorm
    }
    
    # Get mood from weather code
    mood = weather_code_map.get(code)
    
    if mood:
        print(f"Weather code {code} mapped to mood: {mood}")
    else:
        print(f"Unknown weather code {code}, using temperature-based mapping")
        # Fallback to temperature-based mood
        if temp < 5:
            mood = "ambient"
        elif temp > 30:
            mood = "summer vibes"
        else:
            mood = "chill"
    
    # Temperature overrides for extreme conditions
    if temp < 0:
        mood = "ambient"
    elif temp > 35:
        mood = "summer vibes"
    
    return mood