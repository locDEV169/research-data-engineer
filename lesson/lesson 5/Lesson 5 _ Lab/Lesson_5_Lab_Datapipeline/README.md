# weather-pipeline — Pipeline mẫu buổi 3 (ETL / ELT → BigQuery)

Project mẫu (lời giải) cho buổi 3: `extract() → transform() → load()` đẩy dữ liệu
thời tiết lên BigQuery. Extract từ **cả CSV lẫn API**; kèm biến thể **ELT** transform
bằng SQL.

## Cấu trúc

```
weather-pipeline/
├── etl/
│   ├── __init__.py
│   ├── extract.py      # extract_csv, extract_api, extract_open_meteo
│   ├── transform.py    # transform (city/temp_c), transform_open_meteo
│   └── load.py         # load() -> BigQuery
├── data/
│   └── weather.csv     # dữ liệu mẫu (có dòng bẩn để transform xử lý)
├── main.py             # run(): điều phối cả 3 bước
├── elt_demo.py         # biến thể ELT: load raw + transform bằng SQL
├── test_connect.py     # pre-work: kiểm tra kết nối BigQuery
├── requirements.txt
├── .gitignore
└── README.md
```

## Chuẩn bị (pre-work)

```bash
# 1. Tạo & kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate          # mac/linux
# .venv\Scripts\activate           # windows

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Trỏ tới key service account (tạm — buổi 4 sẽ dùng .env)
export GOOGLE_APPLICATION_CREDENTIALS="key.json"

# 4. Kiểm tra kết nối
python test_connect.py             # in ra ok = 1 là đạt
```

Trước khi chạy, mở `main.py` đổi `TABLE_CSV` / `TABLE_API` thành
`project.dataset.table` của bạn (dataset phải tồn tại trước).

## Chạy pipeline

```bash
python main.py                 # nguồn CSV (mặc định)
python main.py --source api    # nguồn API (Open-Meteo, Hà Nội)
python elt_demo.py             # biến thể ELT (transform bằng SQL)
```

## Data Source:
https://open-meteo.com/en/docs