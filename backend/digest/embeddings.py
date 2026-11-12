from django.conf import settings
from google.genai import types

from digest.models import EMBEDDING_DIMENSIONS
from digest.vertex import client

def embed(text: str, *, query: bool = False) -> list[float]:
    res = client().models.embed_content(
        model=settings.EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY" if query else "RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )
    values = res.embeddings[0].values if res.embeddings else None
    if not values:
        raise ValueError("empty embedding")
    return values
