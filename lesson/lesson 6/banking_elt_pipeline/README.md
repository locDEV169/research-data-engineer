# Banking ELT Pipeline

Pipeline ELT: `PostgreSQL source -> BigQuery raw -> BigQuery clean -> check kết quả`.

Đây là bản restructure "chuẩn production" của `Lesson_6_Lab_production`: logic ETL
được tách khỏi entrypoint và đóng gói thành package `etl/` cài được qua `pyproject.toml`,
có test thật trong `tests/`. Hành vi pipeline giữ nguyên 100% so với bản gốc.

## 1. Cấu trúc folder

```text
banking_elt_pipeline/
├── pyproject.toml        # khai báo package + dependencies + config pytest
├── requirements.txt      # (không cần nếu đã cài qua pyproject.toml, xem mục 2)
├── .env.example
├── etl/                  # package chứa toàn bộ logic ETL, KHÔNG chứa code chạy trực tiếp
│   ├── settings.py       # đọc .env -> config dict, PROJECT_ROOT
│   ├── tables.py         # khai báo SOURCE_TABLES + METADATA_COLUMNS
│   ├── clients.py        # kết nối Postgres/BigQuery, helper đặt tên bảng, run_sql_file
│   ├── schema.py         # build BigQuery schema cho bảng raw
│   ├── watermark.py      # đọc/ghi watermark theo từng source table
│   ├── hashing.py        # chuẩn hoá giá trị JSON + hash record
│   ├── extract.py        # bước 02: load raw (có run())
│   ├── load.py           # bước 01: init dataset/table BigQuery (có run())
│   ├── transform.py      # bước 03: MERGE raw -> clean (có run())
│   └── checks.py         # bước 04: data quality checks (có run())
├── sql/                  # các file .sql pipeline dùng (DDL, MERGE, checks)
├── scripts/              # entrypoint CLI, mỗi file chỉ gọi vào etl/
│   ├── 00_check_connection.py
│   ├── 01_init_bigquery.py
│   ├── 02_load_raw.py
│   ├── 03_transform_clean.py
│   ├── 04_check_result.py
│   ├── run_pipeline.py
│   └── run_manual_sql.py # chạy tay các file sql trong tests/manual_sql (debug, KHÔNG phải test)
└── tests/                # pytest thật, không cần connect Postgres/BigQuery
    ├── test_extract.py
    ├── test_hashing.py
    └── manual_sql/        # fixture .sql để chạy tay khi debug watermark trên BigQuery thật
```

**Vì sao tách vậy?**

- `etl/` là nơi chứa *logic* — import được, test được, không phụ thuộc việc chạy từ dòng lệnh.
- `scripts/` chỉ là các *entrypoint* mỏng (vài dòng) gọi vào `etl/`. Học viên vẫn chạy
  đúng thứ tự `00 -> 01 -> 02 -> 03 -> 04` như cũ để học từng bước.
- `tests/` là pytest thật (không cần BigQuery/Postgres sống), tách khỏi `manual_sql/`
  là các file `.sql` để chạy tay khi debug trên BigQuery thật.

## 2. `pyproject.toml` là gì?

Là file cấu hình chuẩn của một Python project (thay cho `setup.py` cũ, theo PEP 518/621).
Nó khai báo trong **một file duy nhất**:

- Tên, version, mô tả project.
- Dependencies cần cài (`google-cloud-bigquery`, `pandas`, `psycopg`, ...).
- Package nào cần được cài (ở đây là `etl`).
- Cấu hình các tool khác, ví dụ `[tool.pytest.ini_options]` cho pytest.

Nhờ có nó, lệnh `pip install -e .` sẽ:

1. Cài hết dependencies khai trong `[project.dependencies]`.
2. Cài package `etl/` ở chế độ **editable** (`-e`) — nghĩa là sau này sửa code trong
   `etl/` thì không cần cài lại, `import etl` từ bất kỳ đâu trong máy (kể cả từ
   `scripts/`) đều thấy code mới nhất ngay lập tức.

Đây là lý do `scripts/01_init_bigquery.py` viết được `from etl import load` dù nó nằm
ở thư mục khác với `etl/` — mà không cần chỉnh `sys.path` thủ công.

## 3. Chuẩn bị

```bash
cd "/Users/nguyentienhuy/Documents/JDE/Material/Lesson 6. Production Data Pipeline/banking_elt_pipeline"
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Mở file `.env` và sửa các giá trị:

```bash
SOURCE_DB_HOST=136.110.39.148
SOURCE_DB_PORT=15432
SOURCE_DB_NAME=core_banking
SOURCE_DB_USER=de_source_exporter
SOURCE_DB_PASSWORD=<pw>

GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
BQ_LOCATION=asia-southeast1
HASH_SALT=<strong-random-secret>
```

`BQ_PROJECT_ID` có thể để trống nếu service account JSON có `project_id`.

## 4. Kiểm tra kết nối

```bash
python scripts/00_check_connection.py
```

## 5. Chạy cả pipeline

```bash
python scripts/run_pipeline.py
```

Lệnh này chạy lần lượt:

```bash
python scripts/01_init_bigquery.py
python scripts/02_load_raw.py
python scripts/03_transform_clean.py
python scripts/04_check_result.py
```

Ý nghĩa từng bước (logic nằm trong `etl/`, script chỉ gọi `run()`):

- `01_init_bigquery.py` (`etl/load.py`): tạo dataset và bảng cần dùng trên BigQuery.
- `02_load_raw.py` (`etl/extract.py`): lấy data từ PostgreSQL, append vào BigQuery raw, ghi watermark mới.
- `03_transform_clean.py` (`etl/transform.py`): chạy SQL `MERGE` để tạo bảng clean.
- `04_check_result.py` (`etl/checks.py`): kiểm tra duplicate, null key và reconciliation. Có lỗi thì in đỏ và dừng với exit code khác 0.

## 6. Chạy lần thứ hai

Sau khi source database có dữ liệu mới hoặc update, chạy lại đúng câu lệnh cũ:

```bash
python scripts/run_pipeline.py
```

Không có flag `--mode`. Pipeline chỉ có một đường chạy duy nhất, watermark tự quyết định lấy gì:

- Lần đầu: watermark còn rỗng nên pipeline bỏ mệnh đề `WHERE` và lấy toàn bộ bảng.
- Những lần sau: watermark đã có giá trị nên chỉ lấy `WHERE updated_at > @last_watermark ORDER BY updated_at`.

Watermark được ghi ngay sau khi load raw xong ở bước 02.

> **Sẽ học ở buổi sau:** watermark được ghi *trước* khi bước 04 kiểm tra chất lượng dữ liệu. Nếu bước 04 FAIL, watermark vẫn đã bị ghi và không tự lùi lại.

## 7. BigQuery datasets

- `banking_raw`: append-only, mỗi lần chạy thêm batch mới.
- `banking_clean`: bảng clean/dimensional model, merge idempotent.
- `banking_ops`: chỉ có một bảng `watermarks`, lưu mốc `updated_at` đã load tới của từng source table.

Clean layer hiện có:

- Dimensions: `dim_date`, `dim_customer`, `dim_account`, `dim_branch`, `dim_channel`, `dim_transaction_type`, `dim_currency`, `dim_merchant`.
- Facts: `fact_transaction`, `fact_transaction_status_event`.

## 8. Chạy test thật (pytest)

```bash
pytest
```

Các test trong `tests/test_extract.py` và `tests/test_hashing.py` chỉ test các hàm
thuần (không I/O) như `build_extract_query`, `stable_record_hash` — chạy được ngay,
không cần kết nối Postgres/BigQuery. Đây là điểm khác biệt lớn nhất so với
`test_sql/` của bản gốc (vốn là file `.sql` chạy tay, không phải test tự động) —
giờ nó được giữ lại nguyên vẹn ở `tests/manual_sql/`, chạy qua
`python scripts/run_manual_sql.py` khi cần debug watermark trên BigQuery thật.

## 9. Kiểm tra kết nối source bằng psql

```bash
psql "postgresql://de_source_exporter:<password>@VM_EXTERNAL_IP:15432/core_banking" \
  -c "SELECT count(*) FROM transactions;"
```

User này chỉ được `SELECT`. Không dùng admin user trong bài production.

## 10. Bài học gợi ý

1. Đọc `etl/tables.py` để hiểu danh sách source tables.
2. Đọc `etl/extract.py` để hiểu watermark quyết định lấy dữ liệu nào.
3. Đọc `etl/transform.py` để hiểu ELT transform chạy trong BigQuery.
4. Đọc `sql/02_merge_dimensions.sql` và `sql/03_merge_facts.sql` để hiểu SQL `MERGE`.
5. Chạy `pytest` để thấy test thuần logic không cần DB thật.
6. Chạy pipeline lần thứ hai để quan sát raw append-only nhưng clean không duplicate.
7. Query `banking_ops.watermarks` trước và sau khi chạy để thấy mốc `updated_at` nhích lên.
