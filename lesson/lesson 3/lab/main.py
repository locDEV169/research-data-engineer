"""Lấy 7 kỳ XSMB gần nhất và ghi CSV.

Chạy trong thư mục lab/, sau khi đã export XOSO_API_KEY:

    python main.py
"""

from pathlib import Path

from xsmb.api_client import fetch_until_region_days
from xsmb.config import DAYS, api_key
from xsmb.transform import export_csv, filter_region, latest_draws, to_dataframe

OUTPUT = Path(__file__).resolve().parent / "xsmb_7days.csv"


def main() -> None:
    key = api_key()
    if not key:
        raise SystemExit("Thiếu biến môi trường XOSO_API_KEY")

    draws = fetch_until_region_days(key, days=DAYS)
    latest = latest_draws(filter_region(draws), DAYS)
    if len(latest) < DAYS:
        raise SystemExit(f"Chỉ có {len(latest)} kỳ Miền Bắc, chưa đủ {DAYS}")

    df = to_dataframe(latest)
    if len(df) < DAYS:
        raise SystemExit(f"Chỉ dựng được {len(df)} dòng, chưa đủ {DAYS}")

    export_csv(df, str(OUTPUT))
    print(f"Đã ghi {len(df)} dòng vào {OUTPUT.name}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
