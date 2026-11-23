from pydantic import BaseModel, Field  # pyright: ignore[reportMissingImports]


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Câu hỏi về thuế thu nhập cá nhân.",
        examples=[
            "Thu nhập tính thuế 25 triệu đồng một tháng thì áp dụng thuế suất như thế nào?"
        ],
    )


class HealthResponse(BaseModel):
    message: str
    docs: str


class OpenAICheckResponse(BaseModel):
    status: str
    model: str
    openai_response_preview: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    model: str
    law_count: int
