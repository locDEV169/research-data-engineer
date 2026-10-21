"""Lấy dự báo thời tiết theo giờ tại Hà Nội và ghi CSV.

Chạy trong thư mục lab-weather, sau khi đã cài requirements.txt:

    python main.py
"""

from weather.api import fetch_hourly
from weather.config import OUTPUT
from weather.transform import to_frame


def main() -> None:
    frame = to_frame(fetch_hourly())
    frame.to_csv(OUTPUT, index=False)
    print(f"Đã ghi {len(frame)} dòng vào {OUTPUT.name}")


if __name__ == "__main__":
    main()
