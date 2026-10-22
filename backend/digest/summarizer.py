from enum import StrEnum
from functools import cache

from django.conf import settings
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


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


@cache
def _client() -> genai.Client:
    return genai.Client(
        vertexai=True,
        project=settings.GOOGLE_CLOUD_PROJECT,
        location="global",
    )


def summarize(title: str, excerpt: str) -> Summary:
    res = _client().models.generate_content(
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