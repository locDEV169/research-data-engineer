"""
File __init__.py — biến thư mục 'sales/' thành PACKAGE.
Gom các hàm ra ngoài cho tiện gọi:
    from sales import calculate_revenue, format_vnd
"""

from .calculator import calculate_revenue
from .formatter import format_vnd

__all__ = ["calculate_revenue", "format_vnd"]
