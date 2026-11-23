# ============================================================
# PHẦN 1: Import thư viện để viết API
# ============================================================
from fastapi import Body, FastAPI, HTTPException

from law_service import OPENAI_MODEL, ask_openai, build_laws_context, load_traffic_laws


# ============================================================
# PHẦN 2: Tạo app FastAPI
# ============================================================
app = FastAPI(
    title="Demo API Chatbot Luật giao thông",
    description="Demo thật đơn giản: viết API bằng FastAPI, chạy bằng Uvicorn, test bằng Swagger.",
    version="1.0.0",
)


# ============================================================
# PHẦN 3: API số 1 - kiểm tra API có chạy không
# ============================================================
@app.get("/")
def home():
    return {
        "message": "API chatbot luật giao thông đang chạy.",
        "docs": "Mở Swagger tại http://localhost:8000/docs",
    }


# ============================================================
# PHẦN 4: API số 2 - nhận câu hỏi và trả câu trả lời
# ============================================================
@app.post("/chat")
def chat(
    question: str = Body(
        ...,
        embed=True,
        # min_length=1,
        # max_length=1000,
        # description="Câu hỏi muốn gửi cho chatbot.",
        # examples=["Đi xe máy vượt đèn đỏ bị xử lý như thế nào?"],
    )
):
    try:
        traffic_laws = load_traffic_laws()
        laws_context = build_laws_context(traffic_laws)
        answer = ask_openai(question, laws_context)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {
        "question": question,
        "answer": answer,
        "model": OPENAI_MODEL,
        "law_count": len(traffic_laws),
    }
