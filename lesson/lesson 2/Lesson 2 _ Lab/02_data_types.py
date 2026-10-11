"""
============================================================
 BUỔI 2 · PHẦN 2 — DATA TYPE (KIỂU DỮ LIỆU)
============================================================
Chạy demo:   python 02_data_types.py

Ý chính: Python là kiểu ĐỘNG, không cần khai báo kiểu, kiểu do
GIÁ TRỊ quyết định. Dùng type() để xem, dùng int()/str()/float()
để ép kiểu.
"""

# ------------------------------------------------------------
# 1) Các kiểu cơ bản
# ------------------------------------------------------------
age = 25            # int   - số nguyên
price = 9.99        # float - số thực
name = "Huy"        # str   - chuỗi
active = True        # bool  - True / False
nothing = None       # NoneType - "không có giá trị"

print("age    =", age, "->", type(age))
print("price  =", price, "->", type(price))
print("name   =", name, "->", type(name))
print("active =", active, "->", type(active))
print("nothing=", nothing, "->", type(nothing))

# ------------------------------------------------------------
# 2) Kiểu ĐỘNG: một biến có thể đổi kiểu 
# ------------------------------------------------------------
print("\n--- Kiểu động ---")
x = 10
print("x =", x, type(x))
x = "bây giờ là chuỗi"
print("x =", x, type(x))

# ------------------------------------------------------------
# 3) Ép kiểu (type casting)
# ------------------------------------------------------------
print("\n--- Ép kiểu ---")
so_chuoi = "25"
print('int("25")      =', int(so_chuoi), type(int(so_chuoi)))
print("str(25)        =", str(25), type(str(25)))
print('float("3.14")  =', float("3.14"))
print("int(9.99)      =", int(9.99), "  # cắt phần thập phân, KHÔNG làm tròn")

# Lỗi thường gặp khi demo: ép chuỗi không phải số
print("\n--- Bẫy hay gặp ---")
try:
    int("hai lăm")
except ValueError as e:
    print("int('hai lăm') -> lỗi:", e)

# ------------------------------------------------------------
# 4) Vài phép với chuỗi & số hay dùng trong xử lý data
# ------------------------------------------------------------
print("\n--- Chuỗi & số thường dùng ---")
raw = "  Data Engineer  "
print("strip()  :", repr(raw.strip()))
print("lower()  :", raw.strip().lower())
print("replace  :", "2024-01-15".replace("-", "/"))

# Định dạng chuỗi: 3 cách
# fancy string -> f-string (Python 3.6+)
# .2f -> 2 chữ số thập phân
print("f-string :", f"Xin chào {name}, {age} tuổi, phí {price:.2f}$")

if __name__ == "__main__":
    print("\n>>> Xong phần Data Type.")
