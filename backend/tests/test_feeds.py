from datetime import UTC, datetime

from digest.feeds import parse_feed

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Zenn</title>
<item>
  <title>記事A</title>
  <link>https://zenn.dev/u/articles/a</link>
  <pubDate>Fri, 16 Oct 2026 10:00:00 GMT</pubDate>
  <description>&lt;p&gt;本文です&lt;/p&gt;</description>
</item>
<item>
  <title>日付なし</title>
  <link>https://zenn.dev/u/articles/b</link>
</item>
</channel></rss>"""

def test_parse_feed():
    entries = parse_feed(RSS, "zenn")

    assert len(entries) == 1
    entry = entries[0]
    assert entry.url == "https://zenn.dev/u/articles/a"
    assert entry.published_at == datetime(2026, 10, 16, 10, 0, tzinfo=UTC)
    assert entry.excerpt == "本文です"

from digest.feeds import normalize_url

def test_normalize_url_drops_query_and_fragment():
    url = "https://qiita.com/u/items/abc?utm_source=feed&utm_medium=x#comments"

    assert normalize_url(url) == "https://qiita.com/u/items/abc"