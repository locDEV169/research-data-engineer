"""Gọi API xosoapi.online: lấy 1 trang hoặc nhiều trang có retry khi bị rate limit."""

import logging
import time

import requests  # pyright: ignore[reportMissingModuleSource]

from .config import API_URL

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def fetch_page(page: int, limit: int, api_key: str) -> dict:
    """Gọi 1 trang, trả về response gốc dạng {"success", "data", "meta"}."""
    headers = {"X-API-Key": api_key, "Accept": "application/json"}
    params = {"page": page, "limit": limit}

    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def fetch_all_pages(pages: int, limit: int, api_key: str) -> list[dict]:
    """Lặp qua nhiều trang, gộp trường "data" của từng trang thành 1 list phẳng.

    Khi gặp lỗi 429 (rate limit), chờ theo backoff (1s, 2s, 4s...) rồi thử lại
    tối đa MAX_RETRIES lần trước khi bỏ qua trang đó.
    """
    all_draws: list[dict] = []

    for page in range(1, pages + 1):
        for attempt in range(MAX_RETRIES):
            try:
                payload = fetch_page(page, limit, api_key)
                all_draws.extend(payload["data"])
                logger.info("Đã lấy trang %d/%d (%d bản ghi)", page, pages, len(payload["data"]))
                break

            except requests.exceptions.HTTPError as http_err:
                status = http_err.response.status_code if http_err.response is not None else None
                if status == 429 and attempt < MAX_RETRIES - 1:
                    wait_seconds = 2 ** attempt
                    logger.warning(
                        "Bị rate limit ở trang %d, chờ %ds rồi thử lại...", page, wait_seconds
                    )
                    time.sleep(wait_seconds)
                    continue
                logger.error("Lỗi HTTP ở trang %d: %s", page, http_err)
                break

    return all_draws
