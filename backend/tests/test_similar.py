import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from digest.models import EMBEDDING_DIMENSIONS, Article

def vec(x: float, y: float) -> list[float]:
    return [x, y] + [0.0] * (EMBEDDING_DIMENSIONS - 2)

def make(title: str, embedding: list[float] | None) -> Article:
    return Article.objects.create(
        url=f"https://example.com/{title}",
        title=title,
        source="zenn",
        published_at=timezone.now(),
        summary="s",
        embedding=embedding,
    )

@pytest.fixture
def articles(db):
    return {
        "a": make("a", vec(1, 0)),
        "b": make("b", vec(0.9, 0.1)),
        "c": make("c", vec(0, 1)),
        "none": make("none", None),
    }

@pytest.mark.django_db
def test_similar_orders_by_distance(articles):
    res = APIClient().get(f"/api/articles/{articles['a'].pk}/similar/")

    assert res.status_code == 200
    assert [r["title"] for r in res.json()] == ["b", "c"]

@pytest.mark.django_db
def test_search(articles, monkeypatch):
    monkeypatch.setattr("digest.views.embed", lambda text, query: vec(0, 1))

    res = APIClient().get("/api/articles/search/", {"q": "anything"})

    assert res.status_code == 200
    assert [r["title"] for r in res.json()] == ["c", "b", "a"]

@pytest.mark.django_db
def test_search_requests_q():
    res = APIClient().get("/api/articles/search/")

    assert res.status_code == 400
