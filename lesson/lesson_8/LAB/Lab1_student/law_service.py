import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
DATA_FILE = BASE_DIR / "traffic_laws.json"
MAX_QUESTION_LENGTH = 1000

LAW_FIELDS = (
    ("Mã quy định", "id"),
    ("Chủ đề", "topic"),
    ("Loại phương tiện", "vehicle_type"),
    ("Nội dung quy định", "content"),
    ("Mức xử phạt", "penalty"),
    ("Nguồn tham khảo", "source"),
    ("Ngày hiệu lực ghi trong dữ liệu mẫu", "effective_date"),
)

SYSTEM_INSTRUCTIONS = """
Bạn là chatbot demo hỏi đáp Luật giao thông Việt Nam.

Quy tắc trả lời:
- Chỉ trả lời dựa trên dữ liệu luật được cung cấp.
- Không sử dụng kiến thức bên ngoài.
- Không tự suy đoán mức phạt.
- Nếu không tìm thấy thông tin, trả lời:
  "Tôi chưa tìm thấy thông tin phù hợp trong bộ dữ liệu."
- Nêu mã quy định và nguồn tham khảo nếu có dùng dữ liệu.
- Trả lời ngắn gọn, dễ hiểu.
- Nhắc rằng kết quả chỉ phục vụ học tập, không thay thế tư vấn pháp lý.
"""


def load_traffic_laws():
    with open(DATA_FILE, encoding="utf-8") as file:
        return json.load(file)


def build_laws_context(traffic_laws):
    law_texts = []

    for law in traffic_laws:
        law_lines = []

        for label, column in LAW_FIELDS:
            law_lines.append(f"{label}: {law[column]}")

        law_texts.append("\n".join(law_lines))

    return "\n\n---\n\n".join(law_texts)


def validate_question(question):
    question = question.strip()

    if not question:
        raise ValueError("Vui lòng nhập câu hỏi.")

    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError("Câu hỏi quá dài. Vui lòng nhập tối đa 1.000 ký tự.")

    return question


def build_user_prompt(question, laws_context):
    return f"""
DỮ LIỆU LUẬT GIAO THÔNG:

{laws_context}

CÂU HỎI CỦA NGƯỜI DÙNG:
{question}
""".strip()


def ask_openai(question, laws_context):
    question = validate_question(question)

    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_api_key_here":
        raise ValueError("Chưa cấu hình OPENAI_API_KEY trong file .env.")

    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            timeout=30,
            default_headers={"Accept-Encoding": "gzip, deflate"},
        )

        return client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            input=build_user_prompt(question, laws_context),
            max_output_tokens=700,
        ).output_text.strip()
    except Exception as error:
        raise RuntimeError(
            "OpenAI API gặp lỗi. Vui lòng kiểm tra API key, model hoặc kết nối mạng."
        ) from error
