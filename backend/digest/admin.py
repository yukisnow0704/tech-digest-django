from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "category", "published_at")
    list_fillter = ("source", "category")
    search_fields = ("title", "summary")
    date_hierarchy = "published_at"
