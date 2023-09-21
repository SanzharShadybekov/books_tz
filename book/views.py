from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from book.models import Book
from favorite.models import Favorite
from review.serializers import ReviewSerializer
from . import serializers


class StandartResultPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'


class BooksViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('author', 'genre',)

    query_param_start_date = openapi.Parameter(
        'start_date',
        openapi.IN_QUERY,
        description='Start date for filtering',
        type=openapi.TYPE_STRING,
    )

    query_param_end_date = openapi.Parameter(
        'end_date',
        openapi.IN_QUERY,
        description='End date for filtering',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[query_param_start_date, query_param_end_date, ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, *kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BookListSerializer
        elif self.action == 'retrieve':
            return serializers.BookDetailSerializer
        elif self.action == 'reviews':
            return ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(publish_date__range=[start_date, end_date])
        return queryset

    # api/v1/books/<id>/reviews/
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def reviews(self, request, pk):
        book = self.get_object()
        user = request.user
        if request.method == 'GET':
            reviews = book.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)

        elif request.method == 'POST':
            if book.reviews.filter(owner=request.user).exists():
                return response.Response({'msg': 'You already reviewed this book!'}, status=400)
            data = request.data
            serializer = ReviewSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user, book=book)
            return response.Response(serializer.data, status=201)

        else:
            if not book.reviews.filter(owner=user).exists():
                return response.Response({'msg': 'You didn\'t reviewed this book!'}, status=400)
            review = book.reviews.get(owner=user)
            review.delete()
            return response.Response({'msg': 'Successfully deleted'}, status=204)

    # api/v1/books/<id>/favorites/
    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        book = self.get_object()  # Book.objects.get(id=pk)
        user = request.user
        favorite = user.favorites.filter(book=book)

        if request.method == 'POST':
            if favorite.exists():
                return response.Response({'msg': 'Already in Favorite'}, status=400)
            Favorite.objects.create(owner=user, book=book)
            return response.Response({'msg': 'Added to Favorite'}, status=201)

        if favorite.exists():
            favorite.delete()
            return response.Response({'msg': 'Deleted from Favorite'}, status=204)
        return response.Response({'msg': 'Book Not Found in Favorite'}, status=404)
