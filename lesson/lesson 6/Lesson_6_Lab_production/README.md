# Banking ELT To BigQuery

Project này dành riêng cho lớp Data Engineer. Mục tiêu là chạy một pipeline ELT đơn giản:

```text
PostgreSQL source -> BigQuery raw -> BigQuery clean -> check kết quả
```

## 1. Chuẩn bị

```bash
cd "/Users/nguyentienhuy/Documents/JDE/Material/Lesson 4/Lesson_4_Lab_production"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Mở file `.env` và sửa các giá trị sau:

```bash
SOURCE_DB_HOST=136.110.39.148
SOURCE_DB_PORT=15432
SOURCE_DB_NAME=core_banking
SOURCE_DB_USER=de_source_exporter
SOURCE_DB_PASSWORD=<pw>

GOOGLE_APPLICATION_CREDENTIALS="/Users/nguyentienhuy/Documents/JDE/Material/Lesson 4/key/project-9d3c9d87-4adc-4d3b-ac1-76e7a27ee93e.json"
BQ_LOCATION=asia-southeast1
HASH_SALT=<strong-random-secret>
```

`BQ_PROJECT_ID` có thể để trống nếu service account JSON có `project_id`.

## 2. Kiểm tra kết nối

```bash
python 00_check_connection.py
```

Script này kiểm tra:

- Có connect được PostgreSQL source không.
- Có connect được BigQuery bằng service account key không.

## 3. Chạy cả pipeline

```bash
python run_pipeline.py
```

`run_pipeline.py` sẽ chạy lần lượt:

```bash
python 01_init_bigquery.py
python 02_load_raw.py
python 03_transform_clean.py
python 04_check_result.py
```

## 4. Chạy từng bước để học

Nếu muốn dạy chậm, chạy đúng bốn lệnh trên theo thứ tự.

Ý nghĩa từng bước:

- `01_init_bigquery.py`: tạo dataset và bảng cần dùng trên BigQuery.
- `02_load_raw.py`: lấy data từ PostgreSQL, append vào BigQuery raw, rồi ghi watermark mới.
- `03_transform_clean.py`: chạy SQL `MERGE` để tạo bảng clean.
- `04_check_result.py`: kiểm tra duplicate, null key và reconciliation. Có lỗi thì in đỏ và dừng với exit code khác 0.

## 5. Chạy lần thứ hai

Sau khi source database có dữ liệu mới hoặc update, chạy lại đúng câu lệnh cũ:

```bash
python run_pipeline.py
```

Không có flag `--mode`. Pipeline chỉ có một đường chạy duy nhất, watermark tự quyết định lấy gì:

- Lần đầu: watermark còn rỗng nên pipeline bỏ mệnh đề `WHERE` và lấy toàn bộ bảng.
- Những lần sau: watermark đã có giá trị nên chỉ lấy `WHERE updated_at > @last_watermark ORDER BY updated_at`.

Watermark được ghi ngay sau khi load raw xong ở bước 02.

> **Sẽ học ở buổi sau:** watermark được ghi *trước* khi bước 04 kiểm tra chất lượng dữ liệu. Nếu bước 04 FAIL, watermark vẫn đã bị ghi và không tự lùi lại. Buổi sau chúng ta sẽ dựng đúng tình huống đó để thấy dữ liệu bị bỏ sót, rồi sửa bằng cách dời việc ghi watermark ra sau khi checks PASS.

## 6. BigQuery datasets

- `banking_raw`: append-only, mỗi lần chạy thêm batch mới.
- `banking_clean`: bảng clean/dimensional model, merge idempotent.
- `banking_ops`: chỉ có một bảng `watermarks`, lưu mốc `updated_at` đã load tới của từng source table.

> ⚠️ **Nếu bạn đã chạy lab bản cũ:** bảng `banking_ops.watermarks` cũ có schema khác (7 cột) nên code mới sẽ lỗi. Xoá ops dataset một lần trước khi chạy:
>
> ```bash
> bq --location=asia-southeast1 rm -r -f -d <PROJECT_ID>:banking_ops
> ```
>
> Xoá xong, mọi watermark trở về rỗng nên lần chạy kế tiếp lấy full cả 11 bảng. Việc này vô hại: `banking_raw` là append-only, còn clean layer dùng `MERGE` + `QUALIFY ROW_NUMBER() = 1` nên không bị nhân đôi. `banking_raw` và `banking_clean` không cần đụng tới.

Clean layer hiện có:

- Dimensions: `dim_date`, `dim_customer`, `dim_account`, `dim_branch`, `dim_channel`, `dim_transaction_type`, `dim_currency`, `dim_merchant`.
- Facts: `fact_transaction`, `fact_transaction_status_event`.

## 7. Kiểm tra kết nối source bằng psql

```bash
psql "postgresql://de_source_exporter:<password>@VM_EXTERNAL_IP:15432/core_banking" \
  -c "SELECT count(*) FROM transactions;"
```

User này chỉ được `SELECT`. Không dùng admin user trong bài production.

## 8. Cấu trúc folder

```text
Lesson_4_Lab_production/
├── config_tables.py
├── helper.py
├── 00_check_connection.py
├── 01_init_bigquery.py
├── 02_load_raw.py
├── 03_transform_clean.py
├── 04_check_result.py
├── run_pipeline.py
└── sql/
```

## 9. Bài học gợi ý

1. Đọc `config_tables.py` để hiểu danh sách source tables.
2. Đọc `02_load_raw.py` để hiểu watermark quyết định lấy dữ liệu nào.
3. Đọc `03_transform_clean.py` để hiểu ELT transform chạy trong BigQuery.
4. Đọc `sql/02_merge_dimensions.sql` và `sql/03_merge_facts.sql` để hiểu SQL `MERGE`.
5. Chạy pipeline lần thứ hai để quan sát raw append-only nhưng clean không duplicate.
6. Query `banking_ops.watermarks` trước và sau khi chạy để thấy mốc `updated_at` nhích lên.
