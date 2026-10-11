"""
LAB — Chương trình tính doanh thu dùng package 'sales'.

Cấu trúc thư mục:
    lab/
    ├── main.py
    └── sales/
        ├── __init__.py
        ├── calculator.py
        └── formatter.py

Chạy (đứng trong thư mục lab/):
    python main.py
"""

from sales import calculate_revenue, format_vnd


def main():
    revenue = calculate_revenue(quantity=50, unit_price=10_000)
    print(f"Doanh thu: {format_vnd(revenue)}")


if __name__ == "__main__":
    main()
