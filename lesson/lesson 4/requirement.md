# Phân tích bài tập: Thời tiết Open-Meteo ra CSV, chuẩn project và Git

Phạm vi phân tích: đề bài tập về nhà số 4 (Project Structure & Git), tài liệu Forecast API tại https://open-meteo.com/en/docs, và pattern đã có ở `lesson/lesson 3/lab/`. Trong repo khoá học chưa có code lesson 4.

Đề bài là hành vi cần đạt. Nguồn dữ liệu đã chốt: thời tiết Open-Meteo, miễn phí, không cần API key.

## 1. Requirement Summary

Tự tay đi hết vòng một Data Engineer làm mỗi ngày: lấy dữ liệu thật từ API, ghi file, để người khác cài và chạy lại được, rồi đưa project lên Git.

Trong phạm vi:

- Gọi một API công khai. Nguồn đã chọn là Open-Meteo.
- Code Python nhận JSON từ API.
- Ghi dữ liệu ra một file CSV.
- Project có `.venv/`, `requirements.txt` sinh bằng `pip freeze > requirements.txt`, `.gitignore` bỏ `.venv/`, `__pycache__/`, `.env`, `README.md`, và `main.py` với `if __name__ == "__main__":`. Tách `utils.py` khi code chính đủ dài để cần tách.
- Tạo repository public mới trên GitHub cá nhân.
- Nộp link repo đó.

Ngoài phạm vi: thiết kế API (lớp có buổi riêng), database, scheduler, UI, API key.

Tiêu chí xong: người khác clone repo, tạo `.venv`, cài từ `requirements.txt`, chạy `python main.py`, và thấy file CSV trên đĩa. Repo public không chứa `.venv/`.

## 2. Business Flow

Người chạy là học viên. Sau khi nộp, giảng viên clone repo và có thể chạy lại hoặc chỉ mở file CSV.

1. Chọn một địa điểm bằng `latitude` và `longitude`.
2. Gọi Forecast API. Tài liệu ghi mặc định dự báo 7 ngày, tối đa 16 ngày.
3. Đọc JSON. Với curl đã pass, phần thời tiết nằm trong `hourly`: các mảng song song (`time`, `temperature_2m`, `relative_humidity_2m`, `dew_point_2m`, `rain`, `pressure_msl`), cùng độ dài.
4. Ghép các mảng đó thành từng dòng.
5. Ghi CSV.
6. Commit code lên repo public mới. `.venv/` không đi lên Git.

Luật lấy từ tài liệu Open-Meteo:

- Endpoint: `GET https://api.open-meteo.com/v1/forecast`.
- Bắt buộc có `latitude` và `longitude`. Endpoint này không nhận tên thành phố.
- Biến theo ngày truyền qua `daily=`. Biến theo giờ truyền qua `hourly=`.
- `timezone` nên đặt tường minh. JSON mẫu trong tài liệu có `utc_offset_seconds: 0` khi mốc thời gian theo UTC.
- Thành công trả một object có `latitude`, `longitude`, `timezone`, rồi `daily` hoặc `hourly`, kèm `daily_units` hoặc `hourly_units`.
- Sai tên biến trả HTTP 400, body dạng `{ "error": true, "reason": "..." }`.
- `weather_code` là số mã WMO. Cột chữ mô tả thời tiết phải tự map ở client. Tài liệu có bảng mã, ví dụ `0` là Clear sky, `61` là Slight rain, `95` là Thunderstorm.
- API miễn phí không cần key. Trang chủ Open-Meteo ghi non-commercial dùng không cần đăng ký: https://open-meteo.com/.
- Nếu URL có tham số `apikey` mà giá trị không phải key có thật, kể cả `apikey=` rỗng, API trả HTTP 400 với `reason` đúng câu `The supplied API key is invalid.` Mã này nằm ở `ApiKeyManager` của Open-Meteo. Host thương mại `customer-api.open-meteo.com` mới là nơi kiểm tra key. API public thấy `apikey` thì chuyển sang host đó.

Request đang dùng, cùng bộ biến giờ với curl Berlin đã pass, chỉ đổi toạ độ sang Hà Nội:

```
curl "https://api.open-meteo.com/v1/forecast?latitude=21.0285&longitude=105.8542&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,rain,pressure_msl&timezone=Asia%2FBangkok"
```

Response thực tế của URL này:

- `timezone` là `Asia/Bangkok`, `timezone_abbreviation` là `GMT+7`, `utc_offset_seconds` là `25200`.
- Toạ độ trả về là tâm ô lưới `21.05448`, `105.898476`, `elevation` `19.0`. Khác toạ độ yêu cầu `21.0285`, `105.8542`. Tài liệu Open-Meteo mô tả đây là tâm ô được dùng để tạo dự báo.
- `hourly.time` chạy từ `2026-10-21T00:00` đến `2026-10-27T23:00`, đủ 168 mốc giờ.
- Đơn vị trong `hourly_units`: `temperature_2m` và `dew_point_2m` là °C, `relative_humidity_2m` là %, `rain` là mm, `pressure_msl` là hPa.

Curl Berlin `52.52`, `13.41` là mẫu trên trang tài liệu và đã pass trước đó. URL Hà Nội thay đúng hai tham số toạ độ. `Asia%2FBangkok` vẫn là `Asia/Bangkok`.

Điểm khác lesson 3: không có API key, không phân trang, không lọc khu vực. JSON của Open-Meteo là các cột song song, chưa phải danh sách bản ghi như từng kỳ xổ số.

## 3. Existing Implementation

Code bài lab nằm trong `lesson/lesson 4/lab-weather/`. `weather/api.py` có `fetch_hourly`, `weather/transform.py` có `to_frame`, `weather/config.py` có `API_URL`, `PARAMS`, `COLUMNS`, `OUTPUT`. `main.py` gọi hai hàm rồi ghi CSV. `test_weather.py` import `PARAMS`, `COLUMNS`, và `to_frame` từ package `weather`.

`lesson/lesson 3/lab/` đã có vòng lặp gọi API, dựng bảng, ghi CSV, và `main()` nằm sau `if __name__ == "__main__":`. `export_csv` ghi `index=False`, `encoding="utf-8-sig"`.

Lệch giữa đề bài 4 và code lesson 3:

| Đề bài 4 | Lesson 3 đang có |
|---|---|
| `main.py`, tách `utils.py` khi cần | Package `xsmb/` với `api_client.py`, `transform.py`, `config.py` |
| `requirements.txt` sinh bằng `pip freeze` | `requests>=2.31` và `pandas>=2.0`, ghi tay |
| `.gitignore` bỏ `.venv/`, `__pycache__/`, `.env` | Bản `xsmb_project/` còn bỏ qua cả file CSV kết quả |
| Repo GitHub cá nhân, public, tạo mới | Bài làm nằm trong repo khoá học |

Lấy thứ tự việc làm từ lesson 3: gọi API, biến thành bảng, ghi CSV, chặn bằng `if __name__`. Lấy layout từ đề bài 4. Một file `main.py` là đủ cho một request và một CSV.

## 4. Technical Impact

| Vùng | Vì sao |
|---|---|
| HTTP client | Một `GET` tới `api.open-meteo.com`. Cần `timeout` và bắt HTTP 400. |
| Transform | `hourly` trong curl đã pass là dict các list cùng độ dài. Dựng bảng từ `payload["hourly"]`, một dòng mỗi giờ. |
| File CSV | Sản phẩm của bài. Nên nằm trong repo để giảng viên mở được mà không cần chạy. |
| File project | `.venv/`, `requirements.txt`, `.gitignore`, `README.md`, `main.py` là hạng mục đề liệt kê. |
| Git | Repo mới, public, trên GitHub cá nhân. Remote của repo khoá học không phải nơi nộp. |

Không đụng database, auth người dùng, CI, hay UI.

Giả thuyết: đề để mở phần hình dạng CSV. Mục 3 trong đề chỉ có tiêu đề “Lưu dữ liệu ra file CSV”. Thành phố, số ngày, và danh sách cột là lựa chọn của bài làm.

## 5. Recommended Design

Khuyến nghị, không phải luật của đề.

Đặt project ở một folder mới, ngoài repo khoá học, rồi `git init` tại folder đó. Repo khoá học đã là một git repo. Để project bên trong dễ đẩy nhầm remote.

```
weather-open-meteo/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
└── hanoi_hourly.csv
```

Dùng URL Hà Nội ở mục 2. Python gửi từng query param, để `requests` tự mã hoá dấu `/` trong timezone. Không thêm `apikey`.

| Param | Giá trị | Ý nghĩa |
|---|---|---|
| `latitude`, `longitude` | `21.0285`, `105.8542` | Hà Nội |
| `hourly` | `temperature_2m,relative_humidity_2m,dew_point_2m,rain,pressure_msl` | Năm biến theo giờ |
| `timezone` | `Asia/Bangkok` | Giờ hiển thị GMT+7, đúng chuỗi timezone trong response |

Luồng trong `main.py`:

1. `requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=30)`, rồi `raise_for_status()`.
2. Lấy `payload["hourly"]`.
3. Dựng bảng từ dict đó. Cột là `time`, `temperature_2m`, `relative_humidity_2m`, `dew_point_2m`, `rain`, `pressure_msl`.
4. Ghi CSV với `index=False`.
5. In số dòng và tên file.

README ghi địa điểm yêu cầu là Hà Nội, timezone là `Asia/Bangkok`, và toạ độ trong response là tâm ô lưới. Curl Berlin chỉ là mẫu tài liệu đã dùng để kiểm tra cách gọi.

`pandas` hợp vì lesson 3 đã dùng để ghi CSV. Thư viện chuẩn `csv` cũng ghi được file này. Một trong hai là đủ.

Đề bài 4 yêu cầu `main.py`, và cho tách `utils.py` khi cần. Một file vẫn chạy đúng bài.

Thư mục bài lab nằm trong repo khoá học. File phân tích ở ngoài project vì đề không yêu cầu nộp file đó.

```
lesson/lesson 4/
├── requirement.md
└── lab-weather/
    ├── .gitignore
    ├── .venv/
    ├── README.md
    ├── requirements.txt
    ├── main.py
    ├── test_weather.py
    ├── hanoi_hourly.csv
    └── weather/
        ├── __init__.py
        ├── config.py
        ├── api.py
        └── transform.py
```

Đây là flat layout trong [tài liệu đóng gói Python](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/): package import được nằm cùng cấp với `README`. Tài liệu ghi flat layout chạy được mà không cần cài package. `src/` layout phải cài package, thường là cài editable, rồi code mới import được. Bài này chấm bằng `python main.py` và `requirements.txt` từ `pip freeze`, nên flat layout khớp đề. `pyproject.toml` là file của project đóng gói lên PyPI. Đề không yêu cầu file đó.

`lab-weather` là thư mục gốc, chỗ chạy lệnh. Dấu `-` hợp lệ trong tên thư mục và không import được, nên package tên `weather`, trùng dữ liệu của bài. Lesson 3 cũng là flat layout, package tên `xsmb`. Bài này không copy tên file của bài xổ số. `weather/api.py` giữ `fetch_hourly`. `weather/transform.py` giữ `to_frame`. `weather/config.py` giữ `API_URL`, `PARAMS`, `COLUMNS`, `OUTPUT`. `main.py` gọi hai hàm, ghi CSV, và giữ `if __name__ == "__main__":`.

`util` không có trong layout của tài liệu đóng gói. Ba module này chỉ phục vụ Open-Meteo.

`main.py` hiện không có API key. Open-Meteo bản này không nhận key. Thêm biến key vào config, rồi gửi kèm request, lặp lại lỗi `The supplied API key is invalid.` Lesson 3 có `api_key()` vì API xổ số bắt header `X-API-Key`. Bài thời tiết không copy hàm đó.

Chạy `python -m unittest` ngay trong `lab-weather/` thì `import weather` thấy package. Thư mục `tests/` là thói quen khi dùng pytest. Project này chưa cài pytest. `python -m unittest discover -s tests` đưa `tests/` lên đầu import path, nên `import weather` có thể không thấy package. File test để ở gốc project, tên `test_weather.py`.

`.gitignore` đúng mục đề yêu cầu:

```
.venv/
__pycache__/
.env
```

`.env` vẫn khai báo dù bài này không có secret. `pip freeze > requirements.txt` chỉ chạy khi `.venv` đang được activate.

README cần ba ý đề nêu: API nào (Open-Meteo Forecast, link tài liệu), cách cài (tạo `.venv`, activate, `pip install -r requirements.txt`), cách chạy (`python main.py`). Thêm thành phố và ý nghĩa các cột.

CSV nên được commit. Bài nộp là link GitHub. File kết quả nằm sẵn thì giảng viên mở được ngay.

Geocoding API (`geocoding-api.open-meteo.com`) đổi tên thành phố ra toạ độ. Hữu ích khi muốn nhập tên thành phố lúc chạy. Với một thành phố cố định, ghi toạ độ trong code là đủ.

## 6. Risks

| Mức | Rủi ro | Lý do |
|---|---|---|
| Cao | `pip freeze` khi chưa bật `.venv` | `requirements.txt` chứa environment của máy đang dùng. Máy khác cài thừa hoặc lệch version. |
| Cao | Commit `.venv/` | Đề yêu cầu bỏ qua thư mục này. Repo nặng, và người khác không dùng lại environment đó. |
| Trung bình | Ghi nguyên JSON ra CSV | `hourly` là các mảng song song. Ghi cả `payload` sẽ không thành bảng từng giờ. |
| Thấp | Kỳ vọng CSV chứa đúng `21.0285`, `105.8542` | Response trả tâm ô lưới `21.05448`, `105.898476`. Hai số này là toạ độ ô dự báo, không phải toạ độ yêu cầu. |
| Trung bình | Bỏ `timezone` | Mốc thời gian theo UTC. Cột ngày có thể lệch so với giờ Việt Nam. |
| Trung bình | Project nằm trong repo khoá học | Link nộp không phải repo cá nhân mới, hoặc lịch sử git bị trộn. |
| Trung bình | Gửi kèm `apikey` rỗng hoặc sai | Đúng lỗi đã gặp: `The supplied API key is invalid.` URL không có `apikey` thì gọi được. Code không gửi param này, không dùng header key của bài xổ số, và không gọi `customer-api.open-meteo.com`. |
| Thấp | HTTP 400 vì sai tên biến | Body có `reason` khác câu invalid key. In nội dung response trước khi dừng là đủ để sửa. |
| Thấp | Free tier giới hạn tần suất | Bài chạy một lần, một thành phố. Chưa cần retry kiểu lesson 3. |

## 7. Missing Requirements

Đề cố ý để mở. Các ý dưới là lựa chọn của bài làm. Đề không định nghĩa:

- Thành phố, hoặc cặp toạ độ.
- Dự báo theo ngày hay theo giờ. Theo giờ, 7 ngày ra khoảng 168 dòng.
- Danh sách cột. Tài liệu có nhiều biến `daily`.
- Tên file CSV.
- File CSV có được commit lên GitHub hay chỉ commit code.
- Hành vi khi mất mạng hoặc API trả 400.
- `weather_code` để số hay map sang chữ.
- Một thành phố hay nhiều thành phố trong cùng một file.

Đề đã chốt: không cần API key, `.venv/` không commit, `requirements.txt` bằng `pip freeze`, repo mới và public.

Lựa chọn đang dùng, không phải luật của đề: Hà Nội `21.0285`, `105.8542`, biến `hourly` như URL mục 2, timezone `Asia/Bangkok`. Bộ cột này không có `weather_code`.

## 8. Clarification Questions

Không có câu cần hỏi giảng viên trước khi code. Đề cho tự chọn nguồn và tự chọn hình dạng CSV.

Bốn ý tự chốt trước khi viết code:

- **Business:** Hà Nội, dữ liệu theo giờ, 168 dòng cho 7 ngày mặc định.
- **API:** Forecast API, biến `hourly` như curl trên, timezone `Asia/Bangkok`, không gửi `apikey`.
- **File nộp:** CSV được commit cùng code.
- **Security / Operations:** không có key. `.env` vẫn có trong `.gitignore` vì đề yêu cầu.

Database và UI không có câu chặn. Chạy local, một lần, không lịch.

## 9. Testing Impact

Chưa cần test tự động. Bài chấm bằng chạy tay và nhìn repo.

1. Activate `.venv`, chạy `python main.py`.
2. CSV có 168 dòng dữ liệu, từ `2026-10-21T00:00` đến `2026-10-27T23:00`, cộng dòng header. Số này đúng với response hiện tại. Ngày bắt đầu đổi khi gọi vào ngày khác.
3. Cột `time` tăng từng giờ. JSON có `timezone` là `Asia/Bangkok` và `utc_offset_seconds` là `25200`.
4. `temperature_2m` và `dew_point_2m` là số. `relative_humidity_2m` nằm trong khoảng 0 đến 100.
5. Tắt mạng: chương trình báo lỗi, không tạo CSV trông như đã lấy được dữ liệu.
6. `git status` không thấy `.venv/` hay `__pycache__/`.
7. Clone repo vào thư mục trống, cài từ `requirements.txt`, chạy lại ra CSV.

## 10. Development Checklist

1. Tạo folder mới ngoài repo khoá học, `git init`.
2. `python3 -m venv .venv`, activate, `pip install requests pandas`.
3. Viết `main.py`: GET đúng bộ param của URL Hà Nội, dựng bảng từ `payload["hourly"]`, ghi CSV, có `if __name__ == "__main__":`.
4. Chạy và mở CSV.
5. Thêm `.gitignore` với `.venv/`, `__pycache__/`, `.env`.
6. `pip freeze > requirements.txt` khi `.venv` đang bật.
7. Viết `README.md`: API, cài đặt, cách chạy, thành phố và các cột.
8. Commit code, `requirements.txt`, `.gitignore`, `README.md`, và file CSV.
9. Tạo repo public mới trên GitHub cá nhân, push.
10. Kiểm tra trên GitHub: không có `.venv/`, có CSV, README đọc được.
11. Nộp link repo.

## 11. Complexity Assessment

**Small.** Một request, không key, không phân trang. Khối lượng thật là kỷ luật project và Git, đúng tiêu đề bài.

Chưa có nợ kỹ thuật cần gỡ. Không có blocker để bắt đầu.

Hai chỗ dễ làm sai dù code chạy: `pip freeze` ngoài `.venv`, và đẩy project vào repo khoá học thay vì repo cá nhân mới.
