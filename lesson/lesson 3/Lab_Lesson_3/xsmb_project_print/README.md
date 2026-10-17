# XSMB Project (bản print)

Lấy kết quả xổ số Miền Bắc (XSMB) từ API `xosoapi.online`, lưu ra JSON và CSV.

Bản này dùng `print()` để thông báo tiến trình thay vì module `logging`, và gọi mỗi trang API 1 lần (không retry khi bị rate limit — nếu lỗi thì bỏ qua trang đó và chạy tiếp).

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

## Cấu trúc project

```
xsmb_project_print/
├── requirements.txt
├── main.py            # CLI entry point
└── xsmb/
    ├── config.py       # API URL, API key
    ├── api_client.py   # gọi API, phân trang; lỗi thì bỏ qua trang, chạy tiếp
    ├── storage.py       # đọc/ghi JSON
    └── transform.py     # lọc theo khu vực, dựng DataFrame, xuất CSV
```
