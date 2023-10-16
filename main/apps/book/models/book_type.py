import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...common.models import BaseMeta, BaseModel
from ..managers.book_type import BookTypeManager
from django.utils import timezone
from django.utils.text import slugify

online = settings.ONLINE
paper = settings.PAPER
audio = settings.AUDIO


class TYPEChoices(models.TextChoices):
    ONLINE = online, _(online)
    PAPER = paper, _(paper)
    AUDIO = audio, _(audio)

def upload_electron_book(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"electron_book/{filename}"

def upload_audio_book(instance, filename):
    filename_without_extension, extension = os.path.splitext(filename.lower())
    timestamp = timezone.now().strftime("%Y-%m-%d.%H-%M-%S")
    filename = f"{slugify(filename_without_extension)}.{timestamp}{extension}"
    return f"audio_book/{filename}"


class BookType(BaseModel):
    """
    The aim of this model is the following:
     - it shows the type and price of a given main
     - e.x:
       Book:
          :type 1 -> online, 10 000
          :type 2 -> hard copy/paper 10 000
          :type 3 -> audio 10 000
    """
    book_type = models.CharField(
        max_length=10, choices=TYPEChoices.choices, default=TYPEChoices.PAPER
    )
    price = models.DecimalField(max_digits=20, decimal_places=2)
    book = models.ForeignKey(
        "book.Book",
        on_delete=models.CASCADE,
        related_name="types",
    )
    # electron_book = models.FileField(upload_to=upload_electron_book)
    # audio_book = models.FileField(upload_to=upload_audio_book)
    objects = BookTypeManager()

    class Meta(BaseMeta):
        verbose_name = _("Book Type")
        verbose_name_plural = _("Book Types")

    def __str__(self) -> str:
        return f"{self.book_type} {self.price}"
