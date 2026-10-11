"""
PHẦN 7 — PACKAGE: file main.py chạy cả pipeline ETL.

Cấu trúc thư mục:
    07_package/
    ├── main.py
    └── etl/                <- đây là PACKAGE (có __init__.py)
        ├── __init__.py
        ├── extract.py
        ├── transform.py
        └── load.py

Chạy demo (đứng trong thư mục 07_package/):
    python main.py

Điểm dạy:
  - Package = thư mục chứa nhiều module + file __init__.py.
  - Import theo dấu chấm: etl.extract, hoặc gọn hơn nhờ __init__.py.
"""

# Cách 1: import qua __init__.py đã gom sẵn (gọn nhất)
from etl import read_csv, clean, save

# Cách 2: import theo đường dẫn package đầy đủ (bỏ chú thích để thử)
# from etl.extract import read_csv
# from etl.transform import clean
# from etl.load import save


def run_pipeline():
    print("=== Chạy pipeline ETL ===")
    raw = read_csv("sales.csv")     # E
    cleaned = clean(raw)            # T
    n = save(cleaned)              # L
    print(f"=== Xong: đã xử lý {n} dòng ===")


if __name__ == "__main__":
    run_pipeline()
