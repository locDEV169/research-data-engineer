"""HTTP package — export app để `uvicorn api:app` vẫn chạy được."""

from api.app import app

__all__ = ["app"]
