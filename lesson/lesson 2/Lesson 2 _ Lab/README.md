# Code demo — Buổi 2 (Python Structure, Venv & Git)

Mỗi phần là một file/thư mục riêng để mentor vừa giảng vừa demo. Tất cả đều
chạy được với `python <file>.py`, không cần cài thư viện ngoài.

## Thứ tự demo

| # | File / thư mục | Nội dung | Lệnh chạy |
|---|----------------|----------|-----------|
| 1 | `01_compile_interpret.py` | Python biên dịch hay thông dịch? + kiểm tra CPython | `python 01_compile_interpret.py` |
| 2 | `02_data_types.py` | int, float, str, bool, None, ép kiểu | `python 02_data_types.py` |
| 3 | `03_data_structures.py` | list · tuple · dict · set | `python 03_data_structures.py` |
| 4 | `04_functions.py` | hàm, tham số mặc định, *args/**kwargs | `python 04_functions.py` |
| 5 | `05_loops_conditions.py` | for/while, if, list comprehension | `python 05_loops_conditions.py` |
| 6 | `06_module/` | module, import, `if __name__ == "__main__"` | xem dưới |
| 7 | `07_package/` | package, `__init__.py`, pipeline ETL | xem dưới |

## Phần 1 — mẹo kiểm tra CPython nhanh (không cần file)

```bash
python -c "import platform; print(platform.python_implementation())"
# -> CPython

python -c "import sys; print(sys.implementation.name)"
# -> cpython
```

Trong file `01_compile_interpret.py` có demo sâu hơn: `compile()` biến mã nguồn
thành *code object*, `dis.dis()` cho xem **bytecode**, và `py_compile` sinh file
`.pyc` trong `__pycache__/`. Đây là bằng chứng "Python vừa biên dịch (ra
bytecode) vừa thông dịch (chạy bytecode bằng máy ảo PVM)".

## Phần 6 — module & `__main__`

```bash
cd 06_module
python utils.py    # khối test trong utils.py CÓ chạy (vì chạy trực tiếp)
python main.py     # import utils -> khối test KHÔNG chạy, chỉ main() chạy
```

## Phần 7 — package ETL

```bash
cd 07_package
python main.py     # chạy cả pipeline: extract -> transform -> load
```

## Demo Virtual Environment (phần 3 của slide)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install requests
pip freeze > requirements.txt
deactivate
```

## Demo Git (phần 4 của slide)

```bash
git init
git add .
git commit -m "Khởi tạo project demo buổi 2"
# tạo repo trên GitHub rồi:
git remote add origin <URL>
git push -u origin main
```

> `.gitignore` mẫu đã có sẵn trong thư mục này (bỏ qua `.venv/`, `__pycache__/`, `.env`).
