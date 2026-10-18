"""Lọc Miền Bắc, lấy các ngày gần nhất, dựng DataFrame và ghi CSV."""

import pandas as pd  # pyright: ignore[reportMissingImports]

from .config import DAYS, REGION_NAME


def filter_region(draws: list[dict], region_name: str = REGION_NAME) -> list[dict]:
    return [d for d in draws if d["province"]["region"]["name"] == region_name]


def latest_draws(draws: list[dict], days: int = DAYS) -> list[dict]:
    """Mỗi ngày một kỳ, lấy `days` ngày mới nhất. Ngày mới đứng trước."""
    ordered = sorted(draws, key=lambda draw: draw["date"], reverse=True)
    picked = []
    seen = set()
    for draw in ordered:
        day = draw["date"][:10]
        if day in seen:
            continue
        seen.add(day)
        picked.append(draw)
        if len(picked) == days:
            break
    return picked


def to_dataframe(draws: list[dict]) -> pd.DataFrame:
    """Cột ngày và 3 giải đầu: Đặc Biệt, Nhất, Nhì."""
    rows = []
    for draw in draws:
        if len(draw["results"]) < 3:
            continue
        rows.append(
            {
                "date": draw["date"],
                "KetquaDB": ", ".join(draw["results"][0]["values"]),
                "KetquaG1": ", ".join(draw["results"][1]["values"]),
                "KetquaG2": ", ".join(draw["results"][2]["values"]),
            }
        )
    return pd.DataFrame(rows)


def export_csv(df: pd.DataFrame, path: str) -> None:
    # utf-8-sig ghi BOM để Excel nhận đúng tiếng Việt.
    df.to_csv(path, index=False, encoding="utf-8-sig")
