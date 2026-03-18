"""
weather.py — Open-Meteo API integration for trail status

Open-Meteo is free and requires no API key.
Docs: https://open-meteo.com/en/docs

This module handles two things:
  1. get_trail_weather(lat, lon)  — fetches raw weather/soil data for a location
  2. calculate_trail_status(trail, weather_data) — turns that data into Open/Caution/Closed

Phase 1 factors:
  - Precipitation last 24h and 72h (mm)
  - Soil moisture (volumetric, m³/m³)
  - Freeze/thaw flag (sub-freezing low + above-freezing high in last 48h)
  - Trail drainage rating (good / moderate / poor)
"""

import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Soil moisture thresholds (m³/m³ volumetric)
SOIL_WET = 0.30        # above this = Caution
SOIL_SATURATED = 0.40  # above this = Closed

# Precipitation thresholds (mm) per drainage quality
# close_24h: close trail if this much rain fell in the last 24 hours
# caution_24h: caution flag if this much rain fell in the last 24 hours
# close_72h: close trail if this much rain fell over the last 3 days
PRECIP_THRESHOLDS = {
    "good":     {"close_24h": 25, "caution_24h": 10, "close_72h": 40},
    "moderate": {"close_24h": 15, "caution_24h":  5, "close_72h": 25},
    "poor":     {"close_24h": 10, "caution_24h":  3, "close_72h": 15},
}


def get_trail_weather(lat, lon):
    """
    Fetch weather and soil moisture data from Open-Meteo for one location.

    Returns the parsed JSON dict, or None if the request fails.
    past_days=3 gives us yesterday + 2 days before that alongside today's forecast.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "precipitation_sum",     # total rain per day (mm)
            "temperature_2m_max",    # high temp (°C) — used for freeze/thaw
            "temperature_2m_min",    # low temp (°C)  — used for freeze/thaw
        ],
        "hourly": "soil_moisture_0_to_1cm",   # top-layer soil moisture (m³/m³)
        "timezone": "America/New_York",
        "past_days": 3,
        "forecast_days": 1,
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=8)
        response.raise_for_status()  # raises an error if the request failed (4xx/5xx)
        return response.json()
    except requests.RequestException:
        # API is down or network issue — caller will fall back to drainage-only guess
        return None


def calculate_trail_status(trail, weather_data):
    """
    Combine weather data + trail drainage rating to produce a status dict:
      {label, color, icon, precip_24h, precip_72h, soil_moisture, freeze_thaw}

    If weather_data is None (API failed), falls back to a drainage-only guess
    and returns None for all weather fields so the template can show a warning.
    """
    drainage = trail["drainage"]

    # --- API failed: fall back to drainage-only guess ---
    if weather_data is None:
        fallback = {
            "good":     {"label": "Open",    "color": "green",  "icon": "🟢"},
            "moderate": {"label": "Caution", "color": "orange", "icon": "🟡"},
            "poor":     {"label": "Closed",  "color": "red",    "icon": "🔴"},
        }
        status = fallback.get(drainage, fallback["moderate"])
        return {**status, "precip_24h": None, "precip_72h": None,
                "soil_moisture": None, "freeze_thaw": None}

    # --- Precipitation (mm) ---
    daily = weather_data.get("daily", {})
    precip_list = [p or 0 for p in daily.get("precipitation_sum", [])]
    precip_24h = precip_list[-1] if precip_list else 0
    precip_48h = sum(precip_list[-2:]) if len(precip_list) >= 2 else precip_24h
    precip_72h = sum(precip_list[-3:]) if len(precip_list) >= 3 else precip_48h

    # --- Freeze / thaw detection ---
    # Freeze/thaw happens when temps dropped below 0°C recently AND are now above 2°C.
    # This softens the trail surface even without rain.
    temp_min = daily.get("temperature_2m_min", [])
    temp_max = daily.get("temperature_2m_max", [])
    recent_min = [t for t in temp_min[-2:] if t is not None]
    recent_max = [t for t in temp_max[-2:] if t is not None]
    freeze_thaw = (
        any(t < 0 for t in recent_min)
        and any(t > 2 for t in recent_max)
    )

    # --- Soil moisture (average last 24 hourly readings) ---
    hourly = weather_data.get("hourly", {})
    sm_vals = [v for v in hourly.get("soil_moisture_0_to_1cm", []) if v is not None]
    avg_soil = (sum(sm_vals[-24:]) / len(sm_vals[-24:])) if sm_vals else 0.2

    # --- Apply thresholds ---
    t = PRECIP_THRESHOLDS.get(drainage, PRECIP_THRESHOLDS["moderate"])

    if precip_24h >= t["close_24h"] or precip_72h >= t["close_72h"] or avg_soil >= SOIL_SATURATED:
        label, color, icon = "Closed", "red", "🔴"
    elif (precip_24h >= t["caution_24h"] or precip_48h >= t["close_24h"]
          or avg_soil >= SOIL_WET or freeze_thaw):
        label, color, icon = "Caution", "orange", "🟡"
    else:
        label, color, icon = "Open", "green", "🟢"

    return {
        "label": label,
        "color": color,
        "icon": icon,
        "precip_24h": round(precip_24h, 1),
        "precip_72h": round(precip_72h, 1),
        "soil_moisture": round(avg_soil, 3),
        "freeze_thaw": freeze_thaw,
    }
