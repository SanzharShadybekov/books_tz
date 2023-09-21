from rest_framework import serializers

from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_email = serializers.ReadOnlyField(source='owner.email')
    book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Review
        fields = ('owner', 'rating', 'text')
