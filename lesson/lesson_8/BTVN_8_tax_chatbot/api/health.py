from fastapi import APIRouter, HTTPException  # pyright: ignore[reportMissingImports]
from tax_service import check_openai_connection

from api.schemas import HealthResponse, OpenAICheckResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/",
    summary="Kiểm tra API đang hoạt động",
    response_model=HealthResponse,
)
def home():
    return {
        "message": "API chatbot thuế thu nhập cá nhân đang chạy.",
        "docs": "Mở Swagger tại http://localhost:8000/docs",
    }


@router.get(
    "/check-openai",
    summary="Kiểm tra kết nối OpenAI API",
    response_model=OpenAICheckResponse,
    responses={
        400: {"description": "Chưa cấu hình OPENAI_API_KEY"},
        500: {"description": "OpenAI auth/model/network lỗi"},
    },
)
def check_openai():
    try:
        return check_openai_connection()
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
