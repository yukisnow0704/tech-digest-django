from functools import cache

from django.conf import settings
from google import genai

@cache
def client() -> genai.Client:
    return genai.Client(
        vertexai=True,
        project=settings.GOOGLE_CLOUD_PROJECT,
        location="global",
    )
