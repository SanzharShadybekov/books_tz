from django.db import models
from book.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class Mark:
    marks = ((1, 'Too bad!'), (2, 'Bad!'), (3, 'Normal!'), (4, 'Good!'),
             (5, 'Excellent!'))


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=Mark.marks)
    text = models.TextField(blank=True, max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'book']
