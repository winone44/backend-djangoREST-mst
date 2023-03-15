from rest_framework.viewsets import ModelViewSet

from myapp.models import Article, Comment
from myapp.serializers import ArticleSerializer, CommentSerializer


#
# W widoku(views.py) znajduje się logika stron
#


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by('-id')  # Określamy na jakim zbiorze danych pracujemy 'queryset'
    serializer_class = ArticleSerializer  # Jak obiekty są transformowane na JSON


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()  # Określamy na jakim zbiorze danych pracujemy 'queryset'
    serializer_class = CommentSerializer  # Jak obiekty są transformowane na JSON

    def get_queryset(self):
        # Pobierz id artykułu
        comment_id = self.request.query_params.get('article')
        # Znajdź komentarze do artykułu i sortu w odwrotnej kolejności
        return Comment.objects.filter(article=comment_id).order_by('-created')
