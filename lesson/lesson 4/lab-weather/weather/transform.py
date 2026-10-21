"""Ghép các mảng hourly thành một dòng mỗi giờ."""

import pandas as pd  # pyright: ignore[reportMissingImports]

from weather.config import COLUMNS


def to_frame(hourly: dict) -> pd.DataFrame:
    frame = pd.DataFrame(hourly)
    missing = [name for name in COLUMNS if name not in frame.columns]
    if missing:
        raise ValueError(f"Thiếu cột: {missing}")
    return frame[COLUMNS]
