from pgvector.django import CosineDistance
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .embeddings import embed
from .models import Article
from .serializers import ArticleSerializer, SimilarArticleSerializer

SIMILAR_LIMIT = 5
SEARCH_LIMIT = 10

def nearest(vector, *, limit: int, exclude_pk: int | None = None):
    qs = Article.objects.defer("embedding").filter(embedding__isnull=False)
    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)
    return qs.annotate(distance=CosineDistance("embedding", vector)).order_by("distance")[:limit]

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.defer("embedding")
    serializer_class = ArticleSerializer
    filterset_fields = ["source", "category"]

    @action(detail=True)
    def similar(self, request, pk=None):
        article = self.get_object()
        if article.embedding is None:
            return Response([])
        results = nearest(article.embedding, limit=SIMILAR_LIMIT, exclude_pk=article.pk)
        return Response(SimilarArticleSerializer(results, many=True).data)

    @action(detail=False)
    def search(self, request):
        q = request.query_params.get("q", "").strip()
        if not q:
            raise ValidationError({"q": "検索ワードを指定してください"})
        results = nearest(embed(q, query=True), limit=SEARCH_LIMIT)
        return Response(SimilarArticleSerializer(results, many=True).data)
