"""
Module transform.py — bước T (Transform) trong pipeline ETL.
Làm sạch & chuẩn hoá dữ liệu.
"""


def clean(rows):
    """Bỏ khoảng trắng thừa, viết hoa chữ cái đầu cho name & city."""
    print(f"[transform] làm sạch {len(rows)} dòng")
    result = []
    for r in rows:
        result.append({
            "name": r["name"].strip().title(),
            "city": r["city"].strip().title(),
        })
    return result
