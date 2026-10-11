"""
============================================================
 BUỔI 2 · PHẦN 3 — DATA STRUCTURE (list · tuple · dict · set)
============================================================
Chạy demo:   python 03_data_structures.py

Chọn cấu trúc theo câu hỏi:
  - Cần thứ tự & sửa được?      -> list
  - Cố định, không đổi?         -> tuple
  - Tra theo "key"?            -> dict
  - Loại trùng / phép tập hợp? -> set
"""

# ------------------------------------------------------------
# 1) LIST — có thứ tự, sửa được (hay dùng nhất)
# ------------------------------------------------------------
print("--- LIST ---")
nums = [3, 1, 2]
nums.append(4)          # thêm cuối
nums.sort()             # sắp xếp tại chỗ
print("nums          =", nums)
print("phần tử đầu   =", nums[0])
print("2 phần tử cuối=", nums[-2:])
print("độ dài        =", len(nums))

# ------------------------------------------------------------
# 2) TUPLE — có thứ tự nhưng KHÔNG sửa được (bất biến)
# ------------------------------------------------------------
print("\n--- TUPLE ---")
toa_do = (10.5, 20.7)
print("toa_do        =", toa_do)
lat, lon = toa_do       # unpack
print("lat, lon      =", lat, lon)
try:
    toa_do[0] = 99      # sẽ lỗi vì tuple bất biến
except TypeError as e:
    print("Sửa tuple -> lỗi:", e)

# ------------------------------------------------------------
# 3) DICT — cặp key : value (giống bản ghi JSON)
# ------------------------------------------------------------
print("\n--- DICT ---")
user = {"id": 1, "name": "Huy", "role": "DE"}
print("user          =", user)
print("user['name']  =", user["name"])
user["email"] = "huy@huydata.com"   # thêm key mới
print("sau khi thêm  =", user)
print("get an toàn   =", user.get("phone", "chưa có"))
print("duyệt dict:")
for key, value in user.items():
    print(f"   {key} = {value}")

# ------------------------------------------------------------
# 4) SET — không trùng, không thứ tự
# ------------------------------------------------------------
print("\n--- SET ---")
emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]
unique = set(emails)
print("bỏ trùng      =", unique)
a = {1, 2, 3}
b = {2, 3, 4}
print("giao (a & b)  =", a & b)
print("hợp (a | b)   =", a | b)
print("hiệu (a - b)  =", a - b)

if __name__ == "__main__":
    print("\n>>> Xong phần Data Structure.")
