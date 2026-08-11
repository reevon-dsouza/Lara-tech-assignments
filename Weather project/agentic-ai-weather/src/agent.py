"""Agentic AI Weather — Simple weather agent using OpenWeatherMap & Open-Meteo API."""

import logging
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_URL = os.getenv("OPENWEATHER_API_URL", "https://api.openweathermap.org/data/2.5/weather")
OPEN_METEO_GEO_URL = os.getenv("OPEN_METEO_GEO_URL", "https://geocoding-api.open-meteo.com/v1/search")
OPEN_METEO_WEATHER_URL = os.getenv("OPEN_METEO_WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
RETRIES = 3

WMO_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

log = logging.getLogger("WeatherAgent")


def setup_logger():
    """Set up logging to console and logs/agent.log."""
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    if log.hasHandlers():
        log.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    log.addHandler(handler)

    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_dir, "agent.log"), encoding="utf-8")
    file_handler.setFormatter(fmt)
    log.addHandler(file_handler)


def fetch_weather_open_meteo(city):
    """Fetch weather data from free Open-Meteo API using geocoding."""
    for attempt in range(1, RETRIES + 1):
        try:
            log.info("Attempt %d/%d (Open-Meteo) for '%s'", attempt, RETRIES, city)
            geo_resp = requests.get(
                OPEN_METEO_GEO_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=10,
            )
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                log.error("City '%s' not found via Open-Meteo geocoding.", city)
                return None

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = f"{location.get('name', city)}, {location.get('country', '')}".strip(", ")

            weather_resp = requests.get(
                OPEN_METEO_WEATHER_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                    "wind_speed_unit": "ms",
                },
                timeout=10,
            )
            weather_resp.raise_for_status()
            curr = weather_resp.json().get("current", {})

            weather_code = curr.get("weather_code", 0)
            desc = WMO_DESCRIPTIONS.get(weather_code, "Partly cloudy")

            log.info("Weather data received successfully from Open-Meteo.")
            return {
                "city": city_name,
                "temp": curr.get("temperature_2m", 0.0),
                "humidity": curr.get("relative_humidity_2m", 0),
                "wind": curr.get("wind_speed_10m", 0.0),
                "desc": desc,
            }
        except requests.RequestException as exc:
            log.error("Open-Meteo attempt %d failed: %s", attempt, exc)
            if attempt < RETRIES:
                time.sleep(1)

    return None


def fetch_weather(city, api_key=None):
    """Fetch weather with OpenWeatherMap first if key valid, else Open-Meteo fallback."""
    if api_key:
        params = {"q": city, "appid": api_key, "units": "metric"}
        try:
            log.info("Attempting OpenWeatherMap for '%s'", city)
            resp = requests.get(OPENWEATHER_API_URL, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                log.info("Weather data received from OpenWeatherMap.")
                return {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "desc": data["weather"][0]["description"],
                }
            else:
                log.warning(
                    "OpenWeatherMap returned HTTP %d (%s). Falling back to free Open-Meteo API.",
                    resp.status_code,
                    resp.reason,
                )
        except requests.RequestException as exc:
            log.warning("OpenWeatherMap request error (%s). Falling back to Open-Meteo API.", exc)

    return fetch_weather_open_meteo(city)


def decide(temp):
    """Return a simple weather-based recommendation."""
    if temp < 10:
        return "Cold — wear warm layers."
    if temp <= 25:
        return "Pleasant — enjoy your day!"
    return "Hot — stay hydrated."


def main():
    """Run the weather agent in an interactive loop."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    setup_logger()
    load_dotenv()
    log.info("Agent started.")

    api_key = os.getenv("OPENWEATHER_API_KEY")

    print("\n" + "=" * 45)
    print("  🌤️  AGENTIC AI WEATHER AGENT")
    print("  Type a city name to get weather info.")
    print("  Type 'exit' or 'quit' to exit.")
    print("=" * 45 + "\n")

    while True:
        try:
            city = input("Enter city name: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Agent. Goodbye!")
            break

        if not city:
            continue

        if city.lower() in ("exit", "quit", "q"):
            log.info("Agent stopped by user request.")
            print("Goodbye!")
            break

        weather = fetch_weather(city, api_key)
        if not weather:
            log.warning("Could not get weather data for '%s'.", city)
            print(f"❌ Could not retrieve weather data for '{city}'. Please try another city.\n")
            continue

        advice = decide(weather["temp"])
        print(f"\n📍 {weather['city']}: {weather['desc'].title()}")
        print(f"🌡️  Temp: {weather['temp']}°C | 💧 Humidity: {weather['humidity']}%")
        print(f"💨 Wind: {weather['wind']} m/s")
        print(f"🤖 Advice: {advice}\n")

    log.info("Agent stopped.")


if __name__ == "__main__":
    main()

