from django.db import migrations
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    dependencies = [
        ("digest", "0002_article_excerpt"),
    ]

    operations = [
        VectorExtension(),
    ]