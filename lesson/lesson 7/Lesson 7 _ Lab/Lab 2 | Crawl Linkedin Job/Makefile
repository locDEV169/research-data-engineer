# Makefile — đặt tên ngắn cho những lệnh hay phải gõ.
#
# Cú pháp:
#     ten_lenh:
#     <TAB>lệnh shell
#
# LƯU Ý: dòng lệnh BẮT BUỘC bắt đầu bằng ký tự TAB, gõ dấu cách là báo lỗi
#        "missing separator".


# Tạo môi trường ảo + cài thư viện. Chỉ cần chạy 1 lần.
setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

# Chạy job crawl.
run:
	bash run.sh

# Xem nhanh kết quả vừa crawl.
summary:
	bash scripts/summary.sh

# Xoá kết quả cũ.
clean:
	rm -f data/*.csv
