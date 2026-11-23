#!/bin/bash
#
# summary.sh — xem nhanh file CSV vừa crawl, chỉ bằng lệnh dòng lệnh.
#
# Chạy:  bash scripts/summary.sh

cd "$(dirname "$0")/.."

FILE="data/linkedin_jobs.csv"

if [ ! -f "$FILE" ]; then
    echo "Chưa có $FILE. Chạy: make run"
    exit 1
fi

# $(lenh) = lấy kết quả của lệnh làm giá trị.  $(( )) = phép tính số học.
# wc -l đếm số dòng, trừ 1 vì dòng đầu là tên cột (header).
echo "File   : $FILE"
echo "Số job : $(( $(wc -l < "$FILE") - 1 ))"

echo
echo "--- 3 dòng đầu ---"
head -n 3 "$FILE"

echo
echo "--- Số job theo ngày đăng ---"
# grep -o : chỉ in ra PHẦN KHỚP, không in cả dòng. Ở đây là ngày dạng 2026-09-11.
# Rồi bộ tứ kinh điển của Unix:
#   sort     gom các dòng giống nhau nằm cạnh nhau
#   uniq -c  đếm số dòng trùng (BẮT BUỘC sort trước, vì uniq chỉ gộp dòng liền kề)
#   sort -nr xếp giảm dần theo SỐ
#   head     lấy mấy dòng đầu
grep -o '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' "$FILE" | sort | uniq -c | sort -nr | head -n 5

echo
echo "--- Đếm theo từ khoá trong tiêu đề ---"
# grep -c = đếm số dòng khớp;  -i = không phân biệt hoa thường.
echo "senior : $(grep -ci senior "$FILE")"
echo "intern : $(grep -ci intern "$FILE")"
echo "remote : $(grep -ci remote "$FILE")"
