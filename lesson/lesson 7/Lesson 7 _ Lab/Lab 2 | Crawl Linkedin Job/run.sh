#!/bin/bash
#
# run.sh — chạy job crawl LinkedIn bằng 1 lệnh duy nhất.
#
# Chạy:  bash run.sh
# Hoặc:  chmod +x run.sh && ./run.sh

# 1. Nạp cookie trong file .env vào biến môi trường.
#    Phải dùng `source` chứ không phải `bash .env`:
#    `bash .env` chạy trong shell con rồi shell đó chết -> biến mất luôn.
source .env

# 2. Bật môi trường ảo Python (lần đầu tạo bằng: make setup)
source .venv/bin/activate

# 3. Đặt cấu hình cho script Python.
#    export = đẩy biến xuống tiến trình con, Python đọc lại bằng os.getenv().
#    Nhờ vậy đổi từ khoá mà KHÔNG cần sửa một dòng code Python nào.
export KEYWORDS="data analyst"
export COUNT=25
export OUT="data/linkedin_jobs.csv"

# 4. Chạy script Python.
python3 src/linkedin_jobs_scraper_demo.py
