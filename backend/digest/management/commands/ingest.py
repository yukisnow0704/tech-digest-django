import httpx
from django.core.management.base import BaseCommand

from digest.embeddings import embed
from digest.feeds import FEEDS, fetch_feed
from digest.models import Article
from digest.summarizer import summarize


class Command(BaseCommand):
    help = "RSS から記事を取り込み、要約と embeddingを作る"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=10, help="1回で要約する最大件数")
        parser.add_argument("--skip-summary", action="store_true", help="要約しない")
        parser.add_argument("--skip-embed", action="store_true", help="embedding を作らない")

    def handle(self, *args, **options):
        created = self._fetch()
        summarized, embedded, failed = 0, 0, 0
        if not options["skip_summary"]:
            summarized, ng = self._summarize(options["limit"])
            failed += ng
        if not options["skip_embed"]:
            embedded, ng = self._embed(options["limit"])
            failed += ng
        self.stdout.write(
            self.style.SUCCESS(
                f"created={created} summarized={summarized} "
                f"embedded={embedded} failed={failed}"
            )
        )

    def _fetch(self) -> int:
        created = 0
        for source in FEEDS:
            try:
                entries = fetch_feed(source)
            except httpx.HTTPError as e:
                self.stderr.write(f"[{source}] fetch failed: {e}")
                continue
            for entry in entries:
                _, is_new = Article.objects.get_or_create(
                    url=entry.url,
                    defaults={
                        "title": entry.title,
                        "source": entry.source,
                        "published_at": entry.published_at,
                        "excerpt": entry.excerpt,
                    },
                )
                created += is_new
        return created

    def _summarize(self, limit: int) -> tuple[int, int]:
        ok, ng = 0, 0
        targets = Article.objects.filter(summary="").order_by("-published_at")[:limit]
        for article in targets:
            try:
                result = summarize(article.title, article.excerpt)
            except Exception as e:
                self.stderr.write(f"[{article.pk}] summarize failed: {e}")
                ng += 1
                continue
            article.summary = result.summary
            article.category = result.category.value
            article.save(update_fields=["summary", "category", "updated_at"])
            ok += 1
        return ok, ng
    
    def _embed(self, limit: int) -> tuple[int, int]:
        ok, ng = 0, 0
        targets = (
            Article.objects.exclude(summary="")
            .filter(embedding__isnull=True)
            .order_by("-published_at")[:limit]
        )
        for article in targets:
            try:
                article.embedding = embed(f"{article.title}\n{article.summary}")
            except Exception as e:
                self.stderr.write(f"[{article.pk}] embed failed: {e}")
                ng += 1
                continue
            article.save(update_fields=["embedding", "updated_at"])
            ok += 1
        return ok, ng
