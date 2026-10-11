"""
============================================================
 BUỔI 2 · PHẦN 1 — PYTHON BIÊN DỊCH HAY THÔNG DỊCH?
 + Cách kiểm tra bạn đang chạy CPython
============================================================

Chạy demo:   python 01_compile_interpret.py

Ý tưởng:
  - Nhiều người nói "Python là ngôn ngữ thông dịch" — đúng nhưng CHƯA đủ.
  - Thực tế Python có 2 bước:
        (1) BIÊN DỊCH mã nguồn (.py)  ->  bytecode  (.pyc)
        (2) THÔNG DỊCH bytecode đó bằng máy ảo Python (PVM)
  - "CPython" = bản Python phổ biến nhất, viết bằng ngôn ngữ C.
    Ngoài ra còn có PyPy, Jython, IronPython... cùng chạy code Python
    nhưng "động cơ" bên trong khác nhau.
"""

import sys
import dis
import platform
import py_compile
from pathlib import Path


def line(title=""):
    print("\n" + "=" * 60)
    if title:
        print(title)
        print("=" * 60)


# ------------------------------------------------------------
# 1) BẠN ĐANG CHẠY BẢN PYTHON NÀO? (CPython? PyPy?)
# ------------------------------------------------------------
line("1) KIỂM TRA IMPLEMENTATION (CPython?)")

# Cách 1: platform.python_implementation()  -> 'CPython', 'PyPy', 'Jython'...
print("platform.python_implementation() =", platform.python_implementation())

# Cách 2: sys.implementation.name (chữ thường)
print("sys.implementation.name          =", sys.implementation.name)

# Cách 3: xem version chi tiết + phiên bản C compiler đã build ra Python
print("sys.version                      =", sys.version)

# Cách 4: đường dẫn tới trình thông dịch python đang chạy
print("sys.executable                   =", sys.executable)

# Kiểm tra nhanh: có đúng CPython không?
is_cpython = platform.python_implementation() == "CPython"
print("\n=> Đang chạy CPython?", is_cpython)

# Mẹo kiểm tra siêu nhanh ngoài terminal (không cần file):
#   python -c "import platform; print(platform.python_implementation())"
print('Mẹo terminal: python -c "import platform;'
      ' print(platform.python_implementation())"')


# ------------------------------------------------------------
# 2) BƯỚC BIÊN DỊCH: MÃ NGUỒN -> BYTECODE (code object)
# ------------------------------------------------------------
line("2) compile(): mã nguồn -> code object (bytecode)")

source = "x = 21\ny = x * 2\nprint('Ket qua:', y)"
print("Mã nguồn (chuỗi):")
print(source)

# Hàm dựng sẵn compile() biến chuỗi mã nguồn thành 'code object'
code_obj = compile(source, filename="<demo>", mode="exec")
print("\nKiểu của kết quả compile() =", type(code_obj))   # <class 'code'>

# code object là thứ đã được BIÊN DỊCH, giờ mới đem THÔNG DỊCH bằng exec()
print("Chạy code object bằng exec():")
exec(code_obj)


# ------------------------------------------------------------
# 3) NHÌN TẬN MẮT BYTECODE bằng module dis (disassembler)
# ------------------------------------------------------------
line("3) dis.dis(): xem bytecode mà PVM sẽ thực thi")


def cong(a, b):
    return a + b


print("Bytecode của hàm cong(a, b):\n")
dis.dis(cong)
print("\nMỗi dòng trên là 1 lệnh bytecode (LOAD_FAST, BINARY_ADD/OP,")
print("RETURN_VALUE...) — đây chính là thứ máy ảo Python 'đọc & chạy'.")


# ------------------------------------------------------------
# 4) FILE .pyc: BYTECODE ĐƯỢC LƯU RA ĐĨA (__pycache__)
# ------------------------------------------------------------
line("4) py_compile: sinh file .pyc trong __pycache__")

# Tự biên dịch chính file này ra .pyc để xem
pyc_path = py_compile.compile(__file__)
print("Đã biên dịch file này thành:")
print("  ", pyc_path)

cache_dir = Path(__file__).parent / "__pycache__"
if cache_dir.exists():
    print("\nNội dung thư mục __pycache__:")
    for f in sorted(cache_dir.glob("*.pyc")):
        print("   -", f.name)

print("\nGhi chú:")
print(" - Lần đầu import 1 module, CPython biên dịch .py -> .pyc và cache lại.")
print(" - Lần sau, nếu .py không đổi, nó nạp thẳng .pyc cho nhanh (bỏ bước compile).")
print(" - Vì .pyc là file sinh ra tự động -> ta cho __pycache__/ vào .gitignore.")


# ------------------------------------------------------------
# 5) TÓM TẮT LUỒNG CHẠY
# ------------------------------------------------------------
line("5) TÓM TẮT")
line("5) TÓM TẮT")
line("5) TÓM TẮT")
line("5) TÓM TẮT")
print("""
   file.py  --(compile)-->  bytecode (.pyc)  --(PVM thông dịch)-->  kết quả
   \\_____ biên dịch ____/                    \\____ thông dịch ____/

   CPython = trình biên dịch + máy ảo (PVM), viết bằng C.
   => Python VỪA biên dịch (ra bytecode) VỪA thông dịch (chạy bytecode).
""")

if __name__ == "__main__":
    print(">>> Chạy trực tiếp file 01_compile_interpret.py hoàn tất.")
