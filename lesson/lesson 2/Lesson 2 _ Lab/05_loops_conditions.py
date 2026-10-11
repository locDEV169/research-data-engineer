"""
============================================================
 BUỔI 2 · PHẦN 5 — LOOP & CONDITION (VÒNG LẶP & ĐIỀU KIỆN)
============================================================
Chạy demo:   python 05_loops_conditions.py
"""

# ------------------------------------------------------------
# 1) if / elif / else
# ------------------------------------------------------------
print("--- Điều kiện ---")
for diem in [9, 7, 4]:
    if diem >= 8:
        xep_loai = "Giỏi"
    elif diem >= 5:
        xep_loai = "Đạt"
    else:
        xep_loai = "Chưa đạt"
    print(f"điểm {diem} -> {xep_loai}")

# ------------------------------------------------------------
# 2) for + append (kiểu truyền thống)
# ------------------------------------------------------------
print("\n--- for + if -> lọc số chẵn ---")
nums = [1, 2, 3, 4, 5, 6]
evens = []
for n in nums:
    if n % 2 == 0:
        evens.append(n)
print("evens =", evens)

# ------------------------------------------------------------
# 3) LIST COMPREHENSION — cách Pythonic, rất hay dùng trong DE
# ------------------------------------------------------------
print("\n--- List comprehension ---")
evens2 = [n for n in nums if n % 2 == 0]      # y hệt trên nhưng 1 dòng
squares = [n * n for n in nums]
print("evens2  =", evens2)
print("squares =", squares)

# Biến đổi từng dòng dữ liệu (mô phỏng làm sạch data)
rows = ["  Ha Noi ", "da nang", "  HCM  "]
clean = [r.strip().title() for r in rows]
print("clean   =", clean)

# Dict comprehension
gia = {"ao": 100, "quan": 200}
gia_sau_thue = {k: v * 1.1 for k, v in gia.items()}
print("giá sau thuế =", gia_sau_thue)

# ------------------------------------------------------------
# 4) while — lặp tới khi thoả điều kiện
# ------------------------------------------------------------
print("\n--- while + break/continue ---")
i = 0
while i < 5:
    i += 1
    if i == 2:
        continue          # bỏ qua vòng này
    if i == 4:
        break             # dừng hẳn
    print("i =", i)

# ------------------------------------------------------------
# 5) enumerate & zip — bộ đôi cực hữu ích khi duyệt dữ liệu
# ------------------------------------------------------------
print("\n--- enumerate & zip ---")
ten = ["Huy", "Lan", "Nam"]
for idx, t in enumerate(ten, start=1):
    print(f"  {idx}. {t}")

diem = [9, 8, 7]
for t, d in zip(ten, diem):
    print(f"  {t}: {d}")

if __name__ == "__main__":
    print("\n>>> Xong phần Loop & Condition.")
