# Dự báo thời tiết theo giờ tại Hà Nội

Lấy dự báo từ [Open-Meteo Forecast API](https://open-meteo.com/en/docs). API miễn phí, không cần API key.

Địa điểm yêu cầu: Hà Nội (`latitude=21.0285`, `longitude=105.8542`). Response trả tâm ô lưới gần điểm này, không phải đúng toạ độ đã gửi. Timezone: `Asia/Bangkok` (GMT+7).

Các cột trong `hanoi_hourly.csv`:

| Cột | Đơn vị |
|---|---|
| `time` | ISO8601 |
| `temperature_2m` | °C |
| `relative_humidity_2m` | % |
| `dew_point_2m` | °C |
| `rain` | mm |
| `pressure_msl` | hPa |

## Cài đặt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Trên Windows, bật môi trường ảo bằng `.venv\Scripts\activate`.

## Chạy

```bash
python main.py
```

Script ghi `hanoi_hourly.csv` trong cùng thư mục.
