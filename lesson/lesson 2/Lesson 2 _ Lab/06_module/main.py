"""
PHẦN 6 — MODULE: file main.py
Demo IMPORT & if __name__ == "__main__".

Chạy demo (đứng trong thư mục 06_module/):
    python main.py

Thử thêm để thấy sự khác biệt của __main__:
    python utils.py     # khối test trong utils.py CÓ chạy
    python main.py      # khối test trong utils.py KHÔNG chạy
"""

# 3 kiểu import để minh hoạ:
import utils                          # 1) import cả module -> gọi utils.greet()
from utils import to_snake           # 2) import 1 hàm cụ thể -> gọi to_snake()
# import utils as u                  # 3) đặt alias (bỏ chú thích để thử)


def main():
    print(utils.greet("Huy"))                 # dùng qua tên module
    print("snake:", to_snake("First Name"))   # dùng trực tiếp


# Đây là "cửa vào" chuẩn của một chương trình Python.
# Nhờ dòng này, khi file bị import nơi khác thì main() không tự chạy.
if __name__ == "__main__":
    main()
