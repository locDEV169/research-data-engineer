# BTVN 8 — API Chatbot Thuế Thu Nhập Cá Nhân

FastAPI + OpenAI hỏi đáp thuế TNCN từ `personal_income_tax_laws_300.json` (300 mục).

## Endpoints

| Method | Path | Mô tả |
|--------|------|--------|
| `GET` | `/` | Health check |
| `GET` | `/check-openai` | Kiểm tra kết nối OpenAI (key/model/mạng) |
| `POST` | `/chat` | Nhận `{"question": "..."}` và trả câu trả lời |

## Chuẩn bị

```bash
cd "lesson/lesson_8/BTVN_8_tax_chatbot"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Điền `.env` (không commit):

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5-mini
```

## Chạy local

```bash
# Cách 1 — uvicorn CLI
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Cách 2 — python -m uvicorn
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Cách 3 — chạy file Python trực tiếp
python main.py

# Cách 4 — tương thích lệnh cũ
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## Swagger (test API trên trình duyệt)

Sau khi chạy server, mở:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

Trong Swagger:
1. Mở `GET /` → **Try it out** → **Execute**
2. Mở `POST /chat` → **Try it out** → nhập `question` → **Execute**

## CURL

```bash
curl -X GET http://localhost:8000/

curl -X GET http://localhost:8000/check-openai

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Thu nhập tính thuế 25 triệu đồng một tháng thì áp dụng thuế suất như thế nào?"}'
```

## Cấu trúc

```text
BTVN_8_tax_chatbot/
├── main.py                 # entrypoint: uvicorn main:app / python main.py
├── api/                    # routers tách riêng
│   ├── __init__.py         # export app → uvicorn api:app OK
│   ├── app.py              # tạo FastAPI + include routers
│   ├── schemas.py
│   ├── health.py           # GET /, GET /check-openai
│   └── chat.py             # POST /chat
├── tax_service.py          # business / OpenAI
├── personal_income_tax_laws_300.json
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Nộp bài

1. Deploy VM (chạy nền) theo hướng dẫn lớp.
2. Tạo DOCX ghi họ tên + CURL trỏ URL VM (không dùng localhost khi nộp).
