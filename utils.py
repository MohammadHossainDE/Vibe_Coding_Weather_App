import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # you can rename to WEATHERAPI_KEY if you like

# WeatherAPI endpoint for current weather
API_BASE = "http://api.weatherapi.com/v1/current.json"

def build_params(city: str) -> Dict:
    """Build query parameters for WeatherAPI.com"""
    return {
        "key": API_KEY,  # WeatherAPI uses 'key' instead of 'appid'
        "q": city,       # City name or 'city,country'
        "aqi": "no"      # optional: skip air quality data
    }

def get_weather(city: str) -> Optional[Dict]:
    """Fetch current weather from WeatherAPI.com for the given city."""
    if not API_KEY:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not set. Copy .env.example to .env and add your key."
        )

    params = build_params(city)
    try:
        resp = requests.get(API_BASE, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None)
        }
