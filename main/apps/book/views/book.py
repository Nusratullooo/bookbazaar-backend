from django.shortcuts import get_object_or_404
from rest_framework import generics

from main.apps.book.models.book_type import BookType, TYPEChoices
from main.apps.book.models.review import Review
from ..models.content import Content
from main.apps.book.serializers.book_type import BookTypeSerializer
from ..serializers.content import ContentListForBookTypeSerializer
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from ...common.permissions import CreatePermission  # noqa
from ...common.permissions import (
    UpdateDeletePermission,
    PersonalObjectPermission,
)  # noqa
from ...common.pagination import RelatedBookLimitOffsetPagionation
from ..models.book import AUDIO, ONLINE, Book
from ..serializers.book import (
    BookCreateSerializer,
    BookDetailSerializer,
    BookListSerializer,
    BookPublishedDateSerializer,
    BookUpdateSerializer,
)
from ...order.models import Order
from django.db.models import Sum
from main.apps.order.serializers import OrderListSerializer
from ...book.filters.filterprice import BookFilter
from django.db.models import Max, Min
from rest_framework.response import Response
from django.db.models import Avg
from ...book.serializers.book import BookListSerializer
from ...account.models.user_book import UserBook
from ...account.models.audio_book import AudioBook
from ...account.models.online_book import OnlineBook
from django.http import Http404


class BookCreateAPIView(generics.CreateAPIView):
    model = Book
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CreatePermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


book_create_api_view = BookCreateAPIView.as_view()


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filterset_fields = ["title", "author", "category__guid"]
    search_fields = ["title", "author", "category__title"]


book_list_api_view = BookListAPIView.as_view()


class RelatedBooksListAPIView(generics.ListAPIView):
    pagination_class = RelatedBookLimitOffsetPagionation

    def get_queryset(self):
        book = Book.objects.get(guid=self.kwargs["guid"])
        queryset = (
            Book.objects.filter(category=book.category)
            .exclude(guid=self.kwargs["guid"])
            .order_by("?")
        )
        return queryset

    serializer_class = BookListSerializer


related_book_api_view = RelatedBooksListAPIView.as_view()


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    # authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookDetailSerializer
    # permission_classes = [permissions.AllowAny]
    lookup_field = "guid"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            self.__class__.__name__,
            lookup_url_kwarg,
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj


book_detail_api_view = BookDetailAPIView.as_view()


class UserBookAPIView(generics.ListAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserBook.objects.all()
    serializer_class = BookListSerializer
    lookup_field = "guid"

    def get(self, request, guid):
        # try:
        user_online_books = OnlineBook.objects.get(book__guid=guid)
        user_audio_books = AudioBook.objects.get(book__guid=guid)

        user_audio_online_books = UserBook.objects.filter(book__guid=guid)

        try:
            if user_online_books in user_audio_online_books:
                print(user_online_books in user_audio_online_books)
                return Response({"online": True})
        except OnlineBook.DoesNotExist:
            raise Http404

        try:
            if user_audio_books in user_audio_online_books:
                print(user_audio_books in user_audio_online_books)
                return Response({"audio": True})
        except AudioBook.DoesNotExist:
            raise Http404

        try:
            if user_online_books and user_audio_books in user_audio_online_books:
                print(user_online_books and user_audio_books in user_audio_online_books)
                return Response({"online": True, "audio": True})
        except UserBook.DoesNotExist:
            raise Http404

        # except UserBook.DoesNotExist:
        #     raise Http404


user_book_api_view = UserBookAPIView.as_view()


class BookUpdateAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, UpdateDeletePermission]
    lookup_field = "guid"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


book_update_api_view = BookUpdateAPIView.as_view()


class BookDeleteAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAuthenticated, UpdateDeletePermission]
    lookup_field = "guid"


book_delete_api_view = BookDeleteAPIView.as_view()


class NewAddedBookAPIView(generics.ListAPIView):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookListSerializer
    lookup_field = "guid"


new_added_book_api_view = NewAddedBookAPIView.as_view()


class BestSellerBookAPIView(generics.ListAPIView):
    queryset = Order.objects.annotate(quantity_sum=Sum("quantity")).order_by(
        "-quantity_sum"
    )[:3]
    serializer_class = OrderListSerializer


best_seller_books_api_view = BestSellerBookAPIView.as_view()

from ...book.serializers.book_type import BookTypeSerializer


class AudioBooksAPIView(generics.ListAPIView):
    queryset = Book.objects.filter(types__book_type=AUDIO)
    serializer_class = BookListSerializer


audio_book_api_view = AudioBooksAPIView.as_view()


class OnlineBookAPIView(generics.ListAPIView):
    queryset = Content.objects.filter(book_type=ONLINE)
    serializer_class = ContentListForBookTypeSerializer


online_book_api_view = OnlineBookAPIView.as_view()


class BookPulishedDateFilterAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    search_fields = ["published_date", "category__id"]


book_publisheddate_filter_api_view = BookPulishedDateFilterAPIView.as_view()


class BookFilterAPIView(generics.ListAPIView):
    serializer_class = BookListSerializer
    filter_class = BookFilter
    search_fields = [
        "title",
        "published_date",
    ]

    def get_queryset(self):
        queryset = Book.objects.all()

        if "new-book" in self.request.GET:
            queryset = queryset.order_by("-created_at")

        elif "old-book" in self.request.GET:
            queryset = queryset.order_by("created_at")
            return queryset


book_filter_api_view = BookFilterAPIView.as_view()


class BookPublishedDateView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookPublishedDateSerializer


book_published_date_list = BookPublishedDateView.as_view()


class OldBooksAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_class = BookFilter
    search_fields = [
        "title",
        "published_date",
    ]


old_books_api_view = OldBooksAPIView.as_view()


class BookPriceAPIView(generics.GenericAPIView):
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer

    def get(self, request):
        max_price = BookType.objects.aggregate(Max("price"))
        min_price = BookType.objects.aggregate(Min("price"))

        data = {"max_price": max_price, "min_price": min_price}

        return Response(data)


book_price_api_view = BookPriceAPIView.as_view()
