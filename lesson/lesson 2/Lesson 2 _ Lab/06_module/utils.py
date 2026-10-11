"""
PHẦN 6 — MODULE: file utils.py
Đây là một MODULE (mỗi file .py là một module).
Nó chứa các hàm dùng chung để file khác 'import' lại.
"""


def greet(name):
    return f"Xin chào {name}!"


def to_snake(text):
    return text.strip().lower().replace(" ", "_")


# Dòng này chỉ chạy khi ta chạy TRỰC TIẾP: python utils.py
# Khi utils bị import từ main.py -> khối này KHÔNG chạy.
if __name__ == "__main__":
    print("Đang chạy trực tiếp utils.py (chế độ test):")
    print(greet("Test"))
    print(to_snake("  Data Engineer  "))
