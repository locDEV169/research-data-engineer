"""CLI: lấy kết quả xổ số Miền Bắc từ API, lưu JSON + CSV.

Ví dụ:
    python main.py --pages 3 --limit 100
"""

import argparse

from xsmb.api_client import fetch_all_pages
from xsmb.config import API_KEY
from xsmb.storage import save_json
from xsmb.transform import filter_region, to_dataframe, export_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lấy kết quả xổ số Miền Bắc (XSMB)")
    parser.add_argument("--pages", type=int, default=5, help="Số trang cần lấy (mặc định: 5)")
    parser.add_argument("--limit", type=int, default=100, help="Số bản ghi mỗi trang (mặc định: 100)")
    parser.add_argument("--output-json", default="full_draws.json", help="File JSON đầu ra")
    parser.add_argument("--output-csv", default="xsmb_results.csv", help="File CSV đầu ra")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"Bắt đầu lấy {args.pages} trang (limit={args.limit})...")
    all_draws = fetch_all_pages(pages=args.pages, limit=args.limit, api_key=API_KEY)
    print(f"Tổng cộng lấy được {len(all_draws)} bản ghi")

    save_json(all_draws, args.output_json)
    print(f"Đã lưu dữ liệu thô vào {args.output_json}")

    mien_bac_draws = filter_region(all_draws)
    df = to_dataframe(mien_bac_draws)
    export_csv(df, args.output_csv)
    print(f"Đã lưu {len(df)} dòng kết quả Miền Bắc vào {args.output_csv}")


if __name__ == "__main__":
    main()
