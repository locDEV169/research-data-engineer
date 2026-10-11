"""
File __init__.py — sự tồn tại của file này biến thư mục 'etl/'
thành một PACKAGE (gói) mà Python có thể import.

Có thể để trống. Ở đây ta 'gom' vài hàm ra ngoài cho tiện gọi:
    from etl import read_csv, clean, save
"""

from .extract import read_csv
from .transform import clean
from .load import save

# __all__ khai báo những gì được export khi dùng: from etl import *
__all__ = ["read_csv", "clean", "save"]
