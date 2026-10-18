"""Gọi API xosoapi.online cho đến khi đủ số ngày của một khu vực."""

import time

import requests  # pyright: ignore[reportMissingModuleSource]

from .config import API_URL, DAYS, REGION_NAME
from .transform import filter_region, latest_draws

MAX_RETRIES = 3


def fetch_page(page: int, limit: int, api_key: str) -> dict:
    """Gọi 1 trang, trả về response gốc dạng {"success", "data", "meta"}."""
    headers = {"X-API-Key": api_key, "Accept": "application/json"}
    params = {"page": page, "limit": limit}
    response = requests.get(API_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_page_retry(page: int, limit: int, api_key: str) -> dict:
    """Thử lại tối đa 3 lần khi bị 429. Lần chờ: 1s, 2s, 4s."""
    for attempt in range(MAX_RETRIES):
        try:
            return fetch_page(page, limit, api_key)
        except requests.HTTPError as http_err:
            status = (
                http_err.response.status_code if http_err.response is not None else None
            )
            if status == 429 and attempt < MAX_RETRIES - 1:
                wait_seconds = 2**attempt
                print(
                    f"Bị rate limit ở trang {page}, chờ {wait_seconds}s rồi thử lại..."
                )
                time.sleep(wait_seconds)
                continue
            raise


def fetch_until_region_days(
    api_key: str,
    days: int = DAYS,
    limit: int = 100,
    region_name: str = REGION_NAME,
) -> list[dict]:
    """Gộp data các trang đến khi đủ `days` ngày của region, hoặc hết trang."""
    all_draws: list[dict] = []
    page = 1
    while True:
        payload = fetch_page_retry(page, limit, api_key)
        all_draws.extend(payload["data"])
        found = len(latest_draws(filter_region(all_draws, region_name), days))
        last_page = payload["meta"]["last_page"]
        print(f"Trang {page}/{last_page}: {found}/{days} ngày {region_name}")
        if found >= days or page >= last_page:
            return all_draws
        page += 1
