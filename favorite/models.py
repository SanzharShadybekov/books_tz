from django.contrib.auth import get_user_model
from django.db import models

from book.models import Book

User = get_user_model()


class Favorite(models.Model):
    owner = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'book']
