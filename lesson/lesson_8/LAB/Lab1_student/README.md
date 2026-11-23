#  API Chatbot Luật giao thông Việt Nam

## 1. Chạy server (terminal thứ nhất)

cd "/Users/nguyentienhuy/Documents/JDE/Material/Lesson 8. API 1/Lab1"
uvicorn api:app --reload


## 2. Gọi API bằng curl (mở terminal thứ hai)

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Đi xe máy vượt đèn đỏ bị xử lý như thế nào?"}'


## Lưu ý: 
-s tắt thanh tiến trình
-X chọn method 
-H thêm header
-d là nội dung gửi đi.