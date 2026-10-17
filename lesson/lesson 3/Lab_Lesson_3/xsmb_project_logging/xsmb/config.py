"""Cấu hình chung: API endpoint, API key và logging."""

import logging

API_URL = "https://xosoapi.online/api/v1/vietnam/draws"
API_KEY = "YOUR_API_KEY_HERE"  # TODO: điền API key của bạn vào đây
REGION_NAME = "Miền Bắc"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
