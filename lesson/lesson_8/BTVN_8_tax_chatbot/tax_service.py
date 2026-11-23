import json
import os
from pathlib import Path

from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from openai import OpenAI  # pyright: ignore[reportMissingImports]

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "personal_income_tax_laws_300.json"
MAX_QUESTION_LENGTH = 1000


def _load_settings():
    """Reload .env mỗi lần gọi để đổi key không cần restart process."""
    load_dotenv(BASE_DIR / ".env", override=True)
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    return api_key, model


# Giữ tên cũ cho api.py import (giá trị tại import; /chat và /check-openai dùng _load_settings).
OPENAI_API_KEY, OPENAI_MODEL = _load_settings()

TAX_FIELDS = (
    ("Mã quy định", "id"),
    ("Chủ đề", "topic"),
    ("Đối tượng áp dụng", "vehicle_type"),
    ("Nội dung", "content"),
    ("Ghi chú / mức liên quan", "penalty"),
    ("Nguồn tham khảo", "source"),
    ("Ngày hiệu lực", "effective_date"),
)

SYSTEM_INSTRUCTIONS = """
Bạn là chatbot học tập hỏi đáp về thuế thu nhập cá nhân (TNCN) tại Việt Nam.

Quy tắc trả lời:
- Chỉ trả lời dựa trên dữ liệu thuế được cung cấp trong prompt.
- Không dùng kiến thức bên ngoài và không tự suy diễn số liệu thuế.
- Nếu không tìm thấy thông tin phù hợp, trả lời:
  "Tôi chưa tìm thấy thông tin phù hợp trong bộ dữ liệu."
- Khi dùng dữ liệu, nêu mã quy định (id) và nguồn tham khảo nếu có.
- Trả lời ngắn gọn, dễ hiểu bằng tiếng Việt.
- Nhắc rằng kết quả chỉ phục vụ học tập, không thay thế tư vấn thuế chính thức.
"""


def load_tax_laws():
    if not DATA_FILE.exists():
        raise RuntimeError(f"Không tìm thấy file dữ liệu: {DATA_FILE.name}")

    with open(DATA_FILE, encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise RuntimeError("File dữ liệu thuế rỗng hoặc sai định dạng.")

    return records


def build_tax_context(tax_laws):
    blocks = []
    for item in tax_laws:
        lines = [f"{label}: {item[column]}" for label, column in TAX_FIELDS]
        blocks.append("\n".join(lines))
    return "\n\n---\n\n".join(blocks)


def validate_question(question):
    question = question.strip()
    if not question:
        raise ValueError("Vui lòng nhập câu hỏi.")
    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError("Câu hỏi quá dài. Vui lòng nhập tối đa 1.000 ký tự.")
    return question


def build_user_prompt(question, tax_context):
    return f"""
DỮ LIỆU THUẾ THU NHẬP CÁ NHÂN:

{tax_context}

CÂU HỎI CỦA NGƯỜI DÙNG:
{question}
""".strip()


def _openai_client(api_key):
    return OpenAI(
        api_key=api_key,
        timeout=60,
        default_headers={"Accept-Encoding": "gzip, deflate"},
    )


def check_openai_connection():
    """Gọi OpenAI Responses API ngắn để kiểm tra key + model + mạng."""
    api_key, model = _load_settings()
    if not api_key or api_key == "your_api_key_here":
        raise ValueError("Chưa cấu hình OPENAI_API_KEY trong file .env.")

    try:
        client = _openai_client(api_key)
        response = client.responses.create(
            model=model,
            input="ping",
            max_output_tokens=16,
            store=False,
        )
        output = (response.output_text or "").strip()
        return {
            "status": "ok",
            "model": model,
            "openai_response_preview": output[:120],
        }
    except Exception as error:
        raise RuntimeError(
            "Không kết nối được OpenAI. Kiểm tra API key, model hoặc mạng. "
            f"Chi tiết: {error}"
        ) from error


def ask_openai(question, tax_context):
    question = validate_question(question)
    api_key, model = _load_settings()

    if not api_key or api_key == "your_api_key_here":
        raise ValueError("Chưa cấu hình OPENAI_API_KEY trong file .env.")

    try:
        client = _openai_client(api_key)
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=build_user_prompt(question, tax_context),
            max_output_tokens=700,
        )
        return response.output_text.strip()
    except Exception as error:
        raise RuntimeError(
            "OpenAI API gặp lỗi. Vui lòng kiểm tra API key, model hoặc kết nối mạng. "
            f"Chi tiết: {error}"
        ) from error
