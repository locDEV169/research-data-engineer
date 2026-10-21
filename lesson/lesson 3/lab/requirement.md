# Phân tích bài tập: XSMB 7 ngày gần nhất ra CSV

Phạm vi phân tích: đề bài trong yêu cầu này, notebook `lesson/lesson 3/Lab_Lesson_3/api_xsmb_annotated.ipynb`, và package `lesson/lesson 3/Lab_Lesson_3/xsmb_project/`. Hai bản `xsmb_project_print/` và `xsmb_project_logging/` lặp lại cùng pipeline, khác cách in log.

Đề bài là hành vi cần đạt. Code hiện tại là bài trên lớp, chưa phải bài nộp.

## 1. Requirement Summary

Làm lại quy trình đã học: gọi API xổ số, đưa kết quả vào DataFrame, rồi ghi thành một file CSV thật trên máy.

Giá trị: đây là vòng lặp hàng ngày của Data Engineer — nguồn dữ liệu, làm sạch, ghi file, người khác chạy lại được.

Trong phạm vi:

- Dùng API đã học, tài liệu tại https://xosoapi.online/ket-qua-xo-so/mien-bac.
- Đi đủ các bước đã học trên lớp.
- DataFrame chứa kết quả XSMB của 7 ngày gần nhất.
- Ghi CSV mở được bằng Excel, tiếng Việt không lỗi font.
- Nộp file code (`.ipynb` hoặc `.py`) và file `.csv`.

Ngoài phạm vi (đề không yêu cầu): thiết kế API (có buổi học riêng), database, scheduler, UI.

Tiêu chí xong: chạy lại được, CSV nằm trên đĩa, nội dung là XSMB 7 ngày gần nhất, Excel mở không vỡ chữ Việt.

## 2. Business Flow

Người chạy là học viên. Kích hoạt: chạy notebook hoặc `python <file>.py`.

1. Gọi API kết quả xổ số Việt Nam. API trộn nhiều khu vực trong một danh sách.
2. Xử lý lỗi HTTP, gồm rate limit `429`, và ghép các trang thành một list phẳng.
3. Chỉ giữ bản ghi có `province.region.name == "Miền Bắc"`.
4. Chỉ giữ 7 ngày gần nhất.
5. Dựng DataFrame.
6. Ghi CSV ra đĩa.
7. Mở CSV bằng Excel và kiểm tra tiếng Việt.

Luật đã có trong bài trên lớp:

- Auth là header `X-API-Key`.
- Endpoint thật là `GET https://xosoapi.online/api/v1/vietnam/draws`.
- Query đã học: `page`, `limit`.
- Response dạng `{ success, data: [...], meta: { total, page, last_page } }`.
- Chỉ `extend` phần `data`, không lưu cả response theo trang.
- `results[0]` là Giải Đặc Biệt, `results[1]` là Giải Nhất, `results[2]` là Giải Nhì.
- Mỗi giải có `values` là list số, nối bằng `", "`.

Điểm mới so với buổi học: chốt 7 ngày, và CSV là sản phẩm nộp.

## 3. Existing Implementation

Notebook dừng ở DataFrame. Cell 14 đọc `full_draws.json`, lọc Miền Bắc, lấy 3 giải đầu, rồi `df.head()`. Không ghi CSV, không cắt 7 ngày. Số bản ghi phụ thuộc `PAGES = 5` và `LIMIT = 100` ở cell gọi API.

`xsmb_project/` đã có đủ vòng lặp ghi file:

| File | Vai trò |
|---|---|
| `xsmb/config.py` | URL, API key placeholder, `REGION_NAME = "Miền Bắc"` |
| `xsmb/api_client.py` | `fetch_page`, `fetch_all_pages`, retry 429 với backoff 1s, 2s, 4s |
| `xsmb/storage.py` | `save_json` / `load_json`, `ensure_ascii=False` |
| `xsmb/transform.py` | `filter_region`, `to_dataframe`, `export_csv` |
| `main.py` | CLI `--pages`, `--limit`, `--output-json`, `--output-csv` |

`export_csv` hiện ghi `encoding="utf-8"`, `index=False`. Cùng cách ghi ở cả ba bản project.

Lệch giữa đề và code hiện tại:

| Đề bài | Code hiện tại |
|---|---|
| 7 ngày XSMB gần nhất | Lấy N trang mọi miền, lọc Miền Bắc, giữ hết phần lọc được |
| CSV mở Excel không lỗi font Việt | CSV `utf-8` không BOM. Notebook chưa ghi CSV |
| Nộp cả file `.csv` | `.gitignore` của `xsmb_project/` đang bỏ qua `xsmb_results.csv` |

Nên mở rộng `filter_region` + `to_dataframe` + `export_csv`, không viết pipeline mới. Notebook là bản dễ nộp một file. Package là bản dễ chạy lại và tách bước.

## 4. Technical Impact

| Vùng | Vì sao |
|---|---|
| HTTP client | Vẫn gọi `xosoapi.online`. Cần đủ trang để có 7 kỳ Miền Bắc, không phải một con số trang cố định. |
| Transform | Thêm bước chọn 7 ngày sau khi lọc miền. |
| File CSV | Đổi encoding để Excel nhận UTF-8. Đây là phần đề gọi là trọng tâm. |
| Cấu hình | API key vẫn là placeholder `YOUR_API_KEY_HERE`. Chưa có key thì không gọi được. |
| Notebook hoặc script | Một trong hai là đủ. Không cần cả hai. |

Không đụng database, auth người dùng, CI, hay UI.

Giả thuyết: API không có query theo ngày trong phần đã học. Chỉ thấy `page` và `limit`. Lọc 7 ngày làm ở phía client.

## 5. Recommended Design

Đặt bài làm trong `lesson/lesson 3/lab/`, tách khỏi `Lab_Lesson_3/` để code mẫu trên lớp giữ nguyên.

Cách nhỏ nhất nếu nộp một file: notebook hoặc một file `.py` đi thẳng các bước dưới. Cách khớp package sẵn có: thêm hàm chọn 7 ngày và sửa `export_csv`, rồi `main` gọi hàm đó.

Luồng:

1. `fetch_all_pages` đến khi gom đủ 7 bản ghi Miền Bắc, hoặc tới `meta.last_page`.
2. `filter_region(..., "Miền Bắc")`.
3. Sắp `date` mới nhất trước, lấy 7 bản ghi.
4. `to_dataframe` giữ cột đang có: `date`, `KetquaDB`, `KetquaG1`, `KetquaG2`.
5. `to_csv(path, index=False, encoding="utf-8-sig")`.

`utf-8-sig` ghi BOM ở đầu file. Excel trên Windows dùng BOM để nhận UTF-8. `utf-8` trần thường làm Excel đọc sai tiếng Việt.

`index=False` để CSV không có cột số thứ tự thừa.

Tương thích: sửa `export_csv` đổi hành vi file cũ từ UTF-8 không BOM sang UTF-8 có BOM. File vẫn là CSV, Excel đọc tốt hơn. JSON trung gian giữ `ensure_ascii=False`.

API key: điền local, không commit key thật. Pattern hiện tại là hằng số trong `config.py`.

## 6. Risks

| Mức | Rủi ro | Lý do |
|---|---|---|
| Cao | Không có API key | `API_KEY` đang là `YOUR_API_KEY_HERE`. Mọi bước gọi API dừng trước khi có CSV. |
| Cao | Cắt sai 7 ngày | Đề không nói rõ 7 kỳ quay mới nhất hay 7 ngày lịch. API không dạy filter theo ngày. Lấy cố định 5 trang có thể thiếu hoặc dư kỳ Miền Bắc. |
| Trung bình | Excel lỗi font | Ba bản `export_csv` dùng `utf-8` không BOM. Đúng đề thì cần `utf-8-sig`. |
| Trung bình | Cột kết quả không đủ ý “kết quả XSMB” | Code lớp chỉ lấy 3 giải đầu theo vị trí `results[0..2]`. Đề nói “kết quả XSMB”, không liệt kê giải. |
| Thấp | `429` làm mất trang | Retry 3 lần rồi bỏ trang. Có thể cụt, không đủ 7 ngày, mà chương trình vẫn ghi CSV. |
| Thấp | Key lộ trong file nộp | Notebook lớp để key ngay trong cell. |

Cột lớp hiện là ASCII và chữ số (`date`, `KetquaDB`, …). File mẫu có thể không chứa chữ Việt nào, nên lỗi font chưa lộ cho đến khi có header hoặc giá trị tiếng Việt. Encoding vẫn phải đúng vì đề yêu cầu rõ.

## 7. Missing Requirements

Đề chưa chốt:

- “7 ngày gần nhất” là 7 kỳ Miền Bắc mới nhất, hay mọi ngày lịch trong 7 ngày qua, kể cả ngày không có kỳ.
- Danh sách cột CSV. Ba giải đầu như trên lớp, hay toàn bộ giải.
- Tên file CSV.
- Bắt buộc giữ file JSON trung gian hay chỉ cần CSV.
- `curl` có nằm trong bài nộp hay chỉ là bước học.
- Hành vi khi API trả ít hơn 7 kỳ Miền Bắc.
- API key lấy ở đâu và có được commit không.
- Thứ tự dòng: mới nhất trên cùng hay tăng dần theo ngày.
- Có cần sort unique theo `date` nếu một ngày có hơn một bản ghi Miền Bắc.

## 8. Clarification Questions

**Business**

- 7 ngày là 7 kỳ quay Miền Bắc mới nhất, mỗi kỳ một dòng?
- CSV chỉ cần Giải Đặc Biệt, Nhất, Nhì như buổi học, hay mọi giải?

**API**

- API key dùng key nào, và có đưa key vào file nộp không?
- Khi chưa đủ 7 kỳ sau hết các trang, nộp file thiếu hay coi là lỗi?

**UI (file nộp)**

- Tên file CSV mong muốn là gì?
- Thứ tự dòng trong CSV: ngày mới đứng trước?

**Security**

- Không còn câu chặn ngoài việc giữ key khỏi file nộp.

Database và Operations: không có câu chặn. Chạy local, một lần, không lịch.

## 9. Testing Impact

Chưa có test tự động trong lesson 3.

Kiểm tra tay, đúng thứ tự đề:

1. Chạy notebook hoặc script từ thư mục `lab/` với API key thật.
2. Thấy file CSV trên đĩa, không chỉ DataFrame trên màn hình.
3. Đếm đúng 7 dòng dữ liệu Miền Bắc, ngày mới nhất nằm trong tập đó.
4. Mở bằng Excel: chữ Việt còn đúng nếu file có chữ Việt. Với `utf-8-sig`, mở trực tiếp không cần Import Data.
5. Chạy lần hai vẫn ra file, không phụ thuộc biến nhớ của một session notebook đã tắt.
6. Tắt mạng hoặc key sai: chương trình báo lỗi, không ghi CSV rỗng mà tưởng là thành công.

Regression nếu sửa `xsmb_project`: `python main.py` vẫn ra JSON và CSV. Encoding CSV đổi so với file cũ.

## 10. Development Checklist

1. Có API key local, không ghi key vào file sẽ nộp.
2. Gọi API với header `X-API-Key`, phân trang, retry `429`, gộp `data` thành list phẳng.
3. Lọc `Miền Bắc`.
4. Chọn 7 ngày gần nhất theo quy tắc đã chốt ở mục 8.
5. Dựng DataFrame.
6. `to_csv(..., index=False, encoding="utf-8-sig")`.
7. Mở CSV bằng Excel.
8. Để lại file code và file CSV trong `lesson/lesson 3/lab/`.

## 11. Complexity Assessment

**Small.** Pipeline gọi API, lọc, DataFrame và ghi CSV đã có trong `xsmb_project/`. Phần thêm là cắt 7 ngày và BOM cho Excel.

Chưa biết, không chặn việc viết khung: ý nghĩa chính xác của “7 ngày” và bộ cột. Chặn chạy thật: API key.

Không có nợ kỹ thuật cần xử lý trước. Ba thư mục project giống nhau là tài liệu buổi học, không cần gộp để làm bài này.
