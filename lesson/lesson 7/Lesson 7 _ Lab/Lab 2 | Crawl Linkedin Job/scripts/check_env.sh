#!/bin/bash
#
# check_env.sh — kiểm tra nhanh trước khi crawl: đủ đồ nghề chưa?
#
# Chạy:  bash scripts/check_env.sh

# cd sang thư mục gốc của lab (script này nằm trong scripts/ nên phải lùi 1 cấp)
cd "$(dirname "$0")/.."

# if [ ... ]; then ... fi  là cú pháp rẽ nhánh của bash.
# -f = file có tồn tại không;  dấu ! = phủ định.
if [ ! -f .env ]; then
    echo "Chưa có .env -> chạy: cp .env.example .env  rồi điền cookie vào"
    exit 1      # exit 1 = kết thúc với trạng thái LỖI
fi

# source = nạp file .env vào shell hiện tại, để dùng được $LI_AT bên dưới
source .env

# -z = chuỗi rỗng. Luôn bọc biến trong nháy kép "..." cho an toàn.
if [ -z "$LI_AT" ]; then
    echo "Thiếu LI_AT trong .env"
    exit 1
fi

if [ -z "$LI_JSESSIONID" ]; then
    echo "Thiếu LI_JSESSIONID trong .env"
    exit 1
fi

# -d = thư mục có tồn tại không
if [ ! -d .venv ]; then
    echo "Chưa có môi trường ảo -> chạy: make setup"
    exit 1
fi

# ${#BIEN} = độ dài chuỗi. In độ dài thay vì in cookie để không bị lộ.
echo "OK: cookie đã có (LI_AT dài ${#LI_AT} ký tự)"
echo "Chạy tiếp: make run"
