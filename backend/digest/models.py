from django.db import models


class Article(models.Model):
    class Source(models.TextChoices):
        ZENN = "zenn", "Zenn"
        QIITA = "qiita", "Qiita"

    url = models.URLField(max_length=500, unique=True)
    title = models.CharField(max_length=300)
    source = models.CharField(max_length=10, choices=Source.choices)
    published_at = models.DateTimeField()
    summary = models.TextField(blank=True)
    excerpt = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["-published_at"])]

    def __str__(self) -> str:
        return self.title
