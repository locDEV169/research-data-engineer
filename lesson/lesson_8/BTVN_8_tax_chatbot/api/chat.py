from fastapi import APIRouter, HTTPException  # pyright: ignore[reportMissingImports]
from tax_service import _load_settings, ask_openai, build_tax_context, load_tax_laws

from api.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["Chatbot"])


@router.post(
    "/chat",
    summary="Hỏi đáp thuế thu nhập cá nhân",
    response_model=ChatResponse,
    responses={
        400: {"description": "Câu hỏi không hợp lệ hoặc thiếu API key"},
        500: {"description": "Lỗi đọc dữ liệu hoặc gọi OpenAI"},
    },
)
def chat(payload: ChatRequest):
    try:
        tax_laws = load_tax_laws()
        tax_context = build_tax_context(tax_laws)
        answer = ask_openai(payload.question, tax_context)
        _, model = _load_settings()
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "question": payload.question,
        "answer": answer,
        "model": model,
        "law_count": len(tax_laws),
    }
