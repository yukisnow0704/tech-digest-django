from enum import StrEnum

from django.conf import settings
from google.genai import types
from pydantic import BaseModel, Field

from digest.vertex import client

class Category(StrEnum):
    AI = "ai"
    WEB = "web"
    FRONTEND = "frontend"
    BACKEND = "backend"
    INFRA = "infra"
    DATA = "data"
    SECURITY = "security"
    MOBILE = "mobile"
    OTHER = "other"


class Summary(BaseModel):
    summary: str = Field(description="記事の要約。日本語で3文以内")
    category: Category


PROMPT = """以下の技術記事を要約し、カテゴリを1つ選んでください。

タイトル: {title}
本文抜粋: {excerpt}
"""

def summarize(title: str, excerpt: str) -> Summary:
    res = client().models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=PROMPT.format(title=title, excerpt=excerpt),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Summary,
            temperature=0.2,
        ),
    )
    if not isinstance(res.parsed, Summary):
        raise ValueError(f"unexpected response: {res.text}")
    return res.parsed