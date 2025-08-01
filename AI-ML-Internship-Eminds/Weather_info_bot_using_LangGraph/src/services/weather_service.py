import requests

def get_weather_real(city: str) -> str:
    """
    Fetches current weather for a city using Open-Meteo API.
    Returns a string with weather info or None if not found.
    """
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_resp = requests.get(geo_url, timeout=5)
    if geo_resp.status_code != 200 or not geo_resp.json().get("results"):
        return None
    geo = geo_resp.json()["results"][0]
    lat, lon = geo["latitude"], geo["longitude"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current_weather=true"
    )
    weather_resp = requests.get(weather_url, timeout=5)
    if weather_resp.status_code != 200:
        return None
    weather = weather_resp.json().get("current_weather")
    if not weather:
        return None

    temp = weather["temperature"]
    wind = weather["windspeed"]
    code = weather["weathercode"]
    return f"Temperature: {temp}°C, Wind: {wind} km/h, Weather code: {code}"