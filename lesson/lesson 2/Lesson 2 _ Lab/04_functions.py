"""
============================================================
 BUỔI 2 · PHẦN 4 — FUNCTION (HÀM)
============================================================
Chạy demo:   python 04_functions.py

Hàm = đóng gói logic để TÁI SỬ DỤNG. Viết một lần, gọi nhiều nơi.
"""


# ------------------------------------------------------------
# 1) Hàm cơ bản: tham số + return
# ------------------------------------------------------------
def clean_name(raw, upper=False):
    """Chuẩn hoá tên: bỏ khoảng trắng thừa. upper=True thì viết HOA."""
    name = raw.strip()
    if upper:
        name = name.upper()
    return name


print("clean_name('  huy ')            =", repr(clean_name("  huy ")))
print("clean_name('  huy ', upper=True)=", repr(clean_name("  huy ", upper=True)))


# ------------------------------------------------------------
# 2) Tham số mặc định & tham số theo tên (keyword)
# ------------------------------------------------------------
def tao_ket_noi(host, port=5432, db="postgres"):
    return f"{host}:{port}/{db}"


print("\n--- Tham số mặc định ---")
print(tao_ket_noi("localhost"))                     # dùng mặc định
print(tao_ket_noi("10.0.0.5", db="sales"))          # đổi db, giữ port
print(tao_ket_noi("10.0.0.5", port=5433, db="dw"))  # đổi hết


# ------------------------------------------------------------
# 3) Trả về nhiều giá trị (thực chất là 1 tuple)
# ------------------------------------------------------------
def thong_ke(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)


nho_nhat, lon_nhat, trung_binh = thong_ke([4, 8, 15, 16, 23, 42])
print("\n--- Trả về nhiều giá trị ---")
print(f"min={nho_nhat}, max={lon_nhat}, avg={trung_binh:.2f}")


# ------------------------------------------------------------
# 4) *args / **kwargs — nhận số lượng tham số tuỳ ý (hay gặp trong DE)
# ------------------------------------------------------------
def gom(*args, **kwargs):
    print("args (vị trí) :", args)
    print("kwargs (tên)  :", kwargs)


print("\n--- *args / **kwargs ---")
gom(1, 2, 3, source="csv", rows=100)


# ------------------------------------------------------------
# 5) VÌ SAO cần hàm? -> tránh lặp code
# ------------------------------------------------------------
def to_snake(text):
    return text.strip().lower().replace(" ", "_")


print("\n--- Tái sử dụng thay vì copy-paste ---")
cols = ["First Name", "  Email Address ", "Phone Number"]
print([to_snake(c) for c in cols])

if __name__ == "__main__":
    print("\n>>> Xong phần Function.")
