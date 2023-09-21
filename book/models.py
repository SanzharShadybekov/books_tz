from django.db import models
from django.contrib.auth import get_user_model

from genre.models import Genre

from ckeditor.fields import RichTextField

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='books')
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, related_name='books')
    description = RichTextField()
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT, related_name='products')
    image = models.ImageField(upload_to='images')
    publish_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
