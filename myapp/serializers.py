from rest_framework import serializers

from myapp.models import Article, Comment

#
# Serializery tłumaczą obiekty Pythona na JSON i JSON na obiekty Pythona
#


class ArticleSerializer(serializers.ModelSerializer):
    number_of_comments = serializers.SerializerMethodField()  # Specjalny typ pola, który później musimy policzyć

    class Meta:
        model = Article  # Wybieramy model
        fields = '__all__'  # Wybieramy pola

    def get_number_of_comments(self, obj):  # Metoda dostaje pojedynczy obiekt który jest serializowany (prefix get_)
        return obj.articles.all().count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment  # Wybieramy model
        fields = '__all__'  # Wybieramy pola
