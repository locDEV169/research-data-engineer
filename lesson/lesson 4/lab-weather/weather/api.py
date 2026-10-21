"""Gọi Open-Meteo Forecast API."""

import requests  # pyright: ignore[reportMissingModuleSource]

from weather.config import API_URL, PARAMS


def fetch_hourly() -> dict:
    response = requests.get(API_URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    payload = response.json()
    hourly = payload.get("hourly")
    if not isinstance(hourly, dict):
        raise SystemExit("Response không có hourly")
    return hourly
