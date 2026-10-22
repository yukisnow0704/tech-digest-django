from datetime import UTC, datetime

import pytest
from django.core.management import call_command

from digest.feeds import FeedEntry
from digest.models import Article
from digest.summarizer import Category, Summary

TARGET = "digest.management.commands.ingest"

ENTRY = FeedEntry(
    url="https://zenn.dev/u/articles/a",
    title="A",
    source="zenn",
    published_at=datetime(2026, 10, 16, tzinfo=UTC),
    excerpt="本文",
)


@pytest.fixture
def fake_io(monkeypatch):
    monkeypatch.setattr(f"{TARGET}.FEEDS", {"zenn": "dummy"})
    monkeypatch.setattr(f"{TARGET}.fetch_feed", lambda source: [ENTRY])
    monkeypatch.setattr(
        f"{TARGET}.summarize",
        lambda title, excerpt: Summary(summary="要約", category=Category.AI),
    )


@pytest.mark.django_db
def test_ingest_is_idempotent(fake_io):
    call_command("ingest")
    call_command("ingest")

    assert Article.objects.count() == 1
    article = Article.objects.get()
    assert article.summary == "要約"
    assert article.category == "ai"
