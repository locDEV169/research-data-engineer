# XSMB Project

Lấy kết quả xổ số Miền Bắc (XSMB) từ API `xosoapi.online`, lưu ra JSON và CSV.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy

```bash
python main.py --pages 3 --limit 100
```

Tham số:

| Tham số | Mặc định | Ý nghĩa |
|---|---|---|
| `--pages` | 5 | Số trang cần lấy từ API |
| `--limit` | 100 | Số bản ghi mỗi trang |
| `--output-json` | `full_draws.json` | File JSON lưu dữ liệu thô |
| `--output-csv` | `xsmb_results.csv` | File CSV kết quả Miền Bắc |
| `--log-level` | `INFO` | Mức log: DEBUG/INFO/WARNING/ERROR |

## Cấu trúc project

```
xsmb_project/
├── requirements.txt
├── main.py            # CLI entry point
└── xsmb/
    ├── config.py       # API URL, API key, logging
    ├── api_client.py   # gọi API, phân trang, retry khi rate limit
    ├── storage.py       # đọc/ghi JSON
    └── transform.py     # lọc theo khu vực, dựng DataFrame, xuất CSV
```
