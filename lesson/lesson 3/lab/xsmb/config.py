"""Cấu hình API. Key đọc từ biến môi trường, không ghi vào source."""

import os

API_URL = "https://xosoapi.online/api/v1/vietnam/draws"
REGION_NAME = "Miền Bắc"
DAYS = 7


def api_key() -> str:
    return os.environ.get("XOSO_API_KEY", "")
