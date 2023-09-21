from django.db.models import Avg
from rest_framework import serializers

from review.serializers import ReviewListSerializer
from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    genre_name = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'author_name',
                  'genre', 'genre_name',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context['request'].user
        repr['rating_avg'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        if user.is_authenticated:
            repr['is_favorite'] = user.favorites.filter(book=instance).exists()
        return repr


class BookDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    genre_name = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = Book
        exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating_avg'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = ReviewListSerializer(instance.reviews.all(), many=True).data
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_favorite'] = user.favorites.filter(book=instance).exists()
        return repr
