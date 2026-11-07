"""main.py — điều phối pipeline: extract -> transform -> load.

Chạy:
    python main.py                # nguồn CSV (mặc định)
    python main.py --source api   # nguồn API (Open-Meteo)

Nhớ set biến môi trường trước khi chạy:
    export GOOGLE_APPLICATION_CREDENTIALS="key.json"
Và đổi TABLE_* cho đúng project của bạn.
"""
import argparse

from etl.extract import extract_csv, extract_open_meteo
from etl.transform import transform, transform_open_meteo
from etl.load import load

# TODO: đổi thành project của bạn: "project.dataset.table"
TABLE_CSV = "project-9d3c9d87-4adc-4d3b-ac1.lesson3_practices.weather"
TABLE_API = "project-9d3c9d87-4adc-4d3b-ac1.lesson3_practices.weather_hourly"


def run(source: str = "csv"):
    """Chạy một lượt pipeline theo nguồn được chọn."""
    if source == "csv":
        df = extract_csv("data/weather.csv")
        df = transform(df)
        load(df, TABLE_CSV)
    elif source == "api":
        df = extract_open_meteo()          # Hà Nội
        df = transform_open_meteo(df)
        # TRUNCATE vì Open-Meteo trả rolling 7-ngày mỗi lần gọi — APPEND sẽ nhân đôi dữ liệu
        # khi chạy lặp lại (ví dụ qua cron). Watermark/incremental đúng cách học ở buổi 4.
        load(df, TABLE_API, write_disposition="WRITE_TRUNCATE")
    else:
        raise ValueError(f"source không hợp lệ: {source!r} (dùng 'csv' hoặc 'api')")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline thời tiết buổi 3")
    parser.add_argument("--source", default="csv", choices=["csv", "api"],
                        help="Nguồn dữ liệu: csv (mặc định) hoặc api")
    args = parser.parse_args()
    run(args.source)
