import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_weather(lat, lon):
    key = os.getenv("TOMORROW_API_KEY")
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={key}"
    res = requests.get(url).json()

    values = res["data"]["values"]
    return {
        "condition": str(values["weatherCode"]),
        "temp": values["temperature"]
    }

def weather_to_mood(weather):
    cond = weather["condition"]
    temp = weather["temp"]

    if "rain" in cond:
        return "lo-fi"
    if "snow" in cond:
        return "acoustic"
    if "clear" in cond:
        return "pop"
    if "cloud" in cond:
        return "indie"
    if temp < 5:
        return "ambient"
    if temp > 30:
        return "summer vibes"
    return "chill"
