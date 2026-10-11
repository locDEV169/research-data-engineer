"""
Module extract.py — bước E (Extract) trong pipeline ETL.
Ở đây mô phỏng 'đọc dữ liệu' bằng data giả, không cần file thật.
"""


def read_csv(path="fake.csv"):
    """Giả lập đọc dữ liệu thô từ nguồn."""
    print(f"[extract] đọc dữ liệu từ: {path}")
    rows = [
        {"name": "  Huy  ", "city": "ha noi"},
        {"name": "Lan", "city": "da nang"},
        {"name": " Nam", "city": "hcm "},
    ]
    return rows
