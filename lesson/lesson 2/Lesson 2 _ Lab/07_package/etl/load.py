"""
Module load.py — bước L (Load) trong pipeline ETL.
Mô phỏng 'ghi dữ liệu' ra đích (ở đây chỉ in ra màn hình).
"""


def save(rows, dest="stdout"):
    """Giả lập ghi dữ liệu đã xử lý ra đích."""
    print(f"[load] ghi {len(rows)} dòng vào: {dest}")
    for r in rows:
        print("   ", r)
    return len(rows)
