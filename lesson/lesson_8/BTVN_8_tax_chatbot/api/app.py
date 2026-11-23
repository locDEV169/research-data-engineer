"""FastAPI application — dùng bởi uvicorn api:app hoặc main:app."""

from fastapi import FastAPI  # pyright: ignore[reportMissingImports]

from api.chat import router as chat_router
from api.health import router as health_router

app = FastAPI(
    title="API Chatbot Thuế Thu Nhập Cá Nhân",
    description=(
        "BTVN 8: FastAPI + OpenAI hỏi đáp thuế TNCN từ bộ dữ liệu học tập 300 mục.\n\n"
        "- `GET /` — kiểm tra API đang chạy\n"
        "- `GET /check-openai` — kiểm tra kết nối OpenAI (key/model/mạng)\n"
        "- `POST /chat` — gửi câu hỏi, nhận câu trả lời\n\n"
        "Swagger UI: `/docs` · ReDoc: `/redoc`"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(health_router)
app.include_router(chat_router)
