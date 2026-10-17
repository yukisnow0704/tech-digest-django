import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from digest.models import Article


@pytest.mark.django_db
def test_filter_articles_by_source():
    Article.objects.create(
        url="https://zenn.dev/example/a", title="A", source="zenn", published_at=timezone.now()
    )
    Article.objects.create(
        url="https://qiita.com/example/b", title="B", source="qiita", published_at=timezone.now()
    )

    res = APIClient().get("/api/articles/", {"source": "zenn"})

    assert res.status_code == 200
    body = res.json()
    assert body["count"] == 1
    assert body["results"][0]["title"] == "A"
