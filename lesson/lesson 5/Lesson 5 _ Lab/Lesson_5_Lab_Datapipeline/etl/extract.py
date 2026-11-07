"""Bước EXTRACT — lấy dữ liệu về dưới dạng pandas DataFrame.

Hai nguồn (đúng như slide buổi 3):
  - extract_csv : đọc từ file CSV local.
  - extract_api : gọi một API công khai, parse JSON.
"""
import requests
import pandas as pd


def extract_csv(path: str) -> pd.DataFrame:
    """Đọc file CSV thành DataFrame. pandas tự lo phần I/O."""
    return pd.read_csv(path)


def extract_api(url: str) -> pd.DataFrame:
    """Gọi API (trả JSON dạng list-of-records) thành DataFrame.

    raise_for_status() ném lỗi nếu HTTP != 2xx — buổi 4 sẽ bọc
    retry + exponential backoff quanh chỗ này.
    """
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def extract_open_meteo(lat: float = 21.03, lon: float = 105.85) -> pd.DataFrame:
    """Ví dụ nguồn API thật: nhiệt độ theo giờ từ Open-Meteo (miễn phí, không cần key).

    Trả về DataFrame 2 cột: time, temp_c — để chạy được end-to-end cho phần API.
    Mặc định toạ độ Hà Nội.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    hourly = resp.json()["hourly"]
    return pd.DataFrame(
        {"time": hourly["time"], "temp_c": hourly["temperature_2m"]}
    )
