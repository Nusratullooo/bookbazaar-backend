from email.policy import default
import os
from random import choices

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.book import BookManager
from autoslug import AutoSlugField
from main.apps.book.models.review import Review
from main.apps.book.models.rate import Rate

from django.db.models import Avg


def upload_book_cover(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"book/{filename}"


def upload_file(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"paper_book/{filename}"

def auido_file(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"audio_book/{filename}"


User = get_user_model()
ONLINE = settings.ONLINE
AUDIO = settings.AUDIO
PAPER = settings.PAPER

class CoverTypeChoices(models.TextChoices):
     wirecover = 'Wire cover'
     softcover = 'Soft cover'
     hardcover = 'Hard cover'


class LanguageTypeChoices(models.TextChoices):
    uzbek = 'Uzbek'
    russia = 'Russia'
    english = 'English'

class Book(BaseModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', null=True)
    author = models.CharField(max_length=255, blank=True)
    annotation = models.TextField(blank=True)
    thumbnail = models.ImageField(blank=True, upload_to=upload_book_cover)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, related_name="books"
    )
    language = models.CharField(max_length=100, choices=LanguageTypeChoices.choices, default=LanguageTypeChoices.uzbek)
    color = models.PositiveIntegerField(blank=True)
    number_of_page = models.PositiveIntegerField(null=True)
    age = models.CharField(max_length=100, null=True)
    # hardcover = models.BooleanField(default=False)
    isbn = models.CharField(max_length=100, null=True, blank=True)
    format = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    cover_type = models.CharField(max_length=100, choices=CoverTypeChoices.choices, default=CoverTypeChoices.wirecover)
    short_description = models.TextField(blank=True)
    published_date = models.CharField(max_length=10, null=True, blank=True)
    paper = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )
    objects = BookManager()
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def get_review(self, *args, **kwargs):
        review_count = Review.objects.filter(book__id=self.id)
        rate_avg = Review.objects.filter(book__id=self.id).aggregate(Avg('point'))

        point_one = Review.objects.filter(book__id=self.id, point='1').count()
        point_two = Review.objects.filter(book__id=self.id, point='2').count()
        point_three = Review.objects.filter(book__id=self.id, point='3').count()
        point_four = Review.objects.filter(book__id=self.id, point='4').count()
        point_five = Review.objects.filter(book__id=self.id, point='5').count()

        total = point_one + point_two + point_three + point_four + point_five
        if total == 0:
            point_one_percent = 0
            point_two_percent = 0
            point_three_percent = 0
            point_four_percent = 0
            point_five_percent = 0
            data = {
                'review_count': review_count.count(),
                'rate': 0,

                # rate number
                "point_one": point_one,
                "point_two": point_two,
                "point_three": point_three,
                "point_four": point_four,
                "point_five": point_five,
            }

            return data

        else:
            point_one_percent = (point_one/total)*100
            point_two_percent = (point_two/total)*100
            point_three_percent = (point_three/total)*100
            point_four_percent = (point_four/total)*100
            point_five_percent = (point_five/total)*100

            for key in rate_avg.keys():
                rate_avg[key] = round(rate_avg[key], 1)

            data = {
                'review_count': review_count.count(),
                'rate': rate_avg[key],

                # rate number
                "point_one": point_one,
                "point_two": point_two,
                "point_three": point_three,
                "point_four": point_four,
                "point_five": point_five,

                # percent
                'point_one_percent': round(point_one_percent),
                'point_two_percent': round(point_two_percent),
                'point_three_percent': round(point_three_percent),
                'point_four_percent': round(point_four_percent),
                'point_five_percent': round(point_five_percent),
            }

            return data

    def update_with_types(self, data):
        book_types = data.pop("book_types")
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        self.types.all().delete()
        self.types.create_book_type(book_types)

    @classmethod
    def return_online_books(self):
        from ..models.content import Content

        return Content.objects.filter(book=self.id, book_type=ONLINE)

    @classmethod
    def return_audio_books(self):
        from ..models.content import Content

        return Content.objects.filter(book=self.id, book_type=AUDIO)

    def set_purchased_book_types_true(self, user):
        from ...account.models.user_book import UserBook

        type_list = []
        for book_type in self.types.all():
            is_purchased = False
            reference = ""

            qs = UserBook.objects.filter(
                book=self, owner=user, book_type=book_type.book_type
            )
            if qs.exists():
                is_purchased = True
                reference = qs.first().guid
            data = dict(
                guid=book_type.guid,
                book_type=book_type.book_type,
                price=book_type.price,
                is_purchased=is_purchased,
                reference=reference,
            )
            type_list.append(data)
        return type_list

    class Meta(BaseMeta):
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self) -> str:
        return self.title
