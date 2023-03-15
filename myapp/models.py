from django.db import models

# Create your models here.

# Klasy za pomocą mechanizmu migracji będą odzwierciedlone w bazie danych jako relacje

# W bazie SQLite tworzona będzie tabela Article z kolumnami
# id - tworzona automatycznie, primary_key
# title - wartość znakowa max. 128
# content - wartość text
# updated - wartość DateTime
# created - wartość DateTime

# W bazie SQLite tworzona będzie tabela Comment z kolumnami
# id - tworzona automatycznie, primary_key
# content - wartość text
# updated - wartość DateTime
# created - wartość DateTime
# article - tworzy relacje miedzy Article a Comment


class Article(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        'myapp.Article',
        on_delete=models.CASCADE,
        related_name='articles'
    )

    def __str__(self):
        return str(self.id) + '. date:' + str(self.updated)
