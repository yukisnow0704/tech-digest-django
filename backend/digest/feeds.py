from dataclasses import dataclass
from datetime import UTC, datetime

import feedparser
import httpx
from django.utils.html import strip_tags

FEEDS = {
    "zenn": "https://zenn.dev/feed",
    "qiita": "https://qiita.com/popular-items/feed",
}

USER_AGENT = "tech-digest-django/0.1"


@dataclass(frozen=True)
class FeedEntry:
    url: str
    title: str
    source: str
    published_at: datetime
    excerpt: str


def parse_feed(content: str | bytes, source: str) -> list[FeedEntry]:
    parsed = feedparser.parse(content)
    entries = []
    for e in parsed.entries:
        link = e.get("link")
        published = e.get("published_parsed") or e.get("updated_parsed")
        if not link or not published:
            continue
        entries.append(
            FeedEntry(
                url=link,
                title=e.get("title", "")[:300],
                source=source,
                published_at=datetime(*published[:6], tzinfo=UTC),
                excerpt=strip_tags(e.get("summary", ""))[:2000],
            )
        )
    return entries


def fetch_feed(source: str) -> list[FeedEntry]:
    res = httpx.get(
        FEEDS[source],
        headers={"User-Agent": USER_AGENT},
        timeout=10,
        follow_redirects=True,
    )
    res.raise_for_status()
    return parse_feed(res.content, source)