"""
Module formatter.py — định dạng số tiền để hiển thị.
"""


def format_vnd(amount):
    """Định dạng số tiền theo VNĐ, ví dụ: 500000 -> '500,000 VNĐ'."""
    return f"{amount:,} VNĐ"
