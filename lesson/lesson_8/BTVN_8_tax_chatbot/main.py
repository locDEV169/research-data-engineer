"""Entrypoint chính — `uvicorn main:app` hoặc `python main.py`."""

import uvicorn  # pyright: ignore[reportMissingImports]
from api.app import app

__all__ = ["app"]


if __name__ == "__main__":
    # Dùng string "main:app" để --reload hoạt động đúng.
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
