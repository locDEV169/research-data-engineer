"""URL, toạ độ Hà Nội và đường dẫn CSV. Không có API key."""

from pathlib import Path

API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,rain,pressure_msl",
    "timezone": "Asia/Bangkok",
}
COLUMNS = [
    "time",
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "rain",
    "pressure_msl",
]
OUTPUT = Path(__file__).resolve().parent.parent / "hanoi_hourly.csv"
