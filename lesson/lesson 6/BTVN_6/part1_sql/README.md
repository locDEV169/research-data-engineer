# BTVN 6 — Phần 1 (SQL nghiệp vụ)

SQL trả lời câu hỏi nghiệp vụ trên Postgres `core_banking`.

| File | Câu | Bắt buộc |
|------|-----|----------|
| `q01_customers_hanoi.sql` | KH ở Hà Nội | có |
| `q02_transactions_by_status.sql` | Đếm GD theo status | có |
| `q03_top20_transactions_by_amount.sql` | Top 20 amount + branch | có |
| `q04_top10_customers_success_amount.sql` | Top 10 KH SUCCESS (TK nguồn) | có |
| `q05_transactions_status_changes.sql` | GD đổi status > 2 lần | có |
| `q06_customers_by_segment.sql` | KH theo segment | optional |
| `q07_top10_branches_open_accounts.sql` | Chi nhánh nhiều TK ACTIVE | optional |
| `q08_fail_rate_by_channel.sql` | Tỷ lệ fail theo kênh | optional |
| `q09_daily_volume_last_30_days.sql` | Volume 30 ngày (`transaction_time`) | optional |
| `q10_top5_merchant_categories.sql` | Top 5 merchant_category SUCCESS | optional |

## Chạy thử

```bash
cd "../BTVN_6"
source .venv/bin/activate
python run_part1.py
```

## Ghi chú

- Câu 1: filter đúng literal đề bài `city = 'Hà Nội'`. Nếu 0 row, kiểm tra `SELECT DISTINCT city FROM customers`.
- Câu 5: coi mỗi dòng `transaction_status_history` là một lần đổi trạng thái (`COUNT(*) > 2`).
- Câu 7: “đang mở” = `account_status = 'ACTIVE'` theo Data Dictionary.
- Câu 9: dùng `transaction_time`, không dùng `created_at` / `updated_at`.
