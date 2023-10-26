from django.contrib import admin

from .models.book import Book
from .models.book_type import BookType
from .models.content import Content
from .models.favourite import Favourite
from .models.rate import Rate
from .models.recommendation import Recommendation
from .models.review import Review
from .models.view import View


class ContentTabularAdmin(admin.TabularInline):
    model = Content


class BookTypeTabularAdmin(admin.TabularInline):
    model = BookType


class RateTabularAdmin(admin.TabularInline):
    model = Rate


class ReviewTabularAdmin(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "guid",
        "title",
        "author",
        "category",
        "language",
        # "hardcover",
    )
    list_display_links = ("guid",)
    list_filter = ("author", "category", "language")
    search_fields = ["author", "category", "language"]
    list_editable = ("author", "category", "language")
    inlines = [
        BookTypeTabularAdmin,
        ContentTabularAdmin,
        RateTabularAdmin,
        ReviewTabularAdmin,
    ]


admin.site.register(Book, BookAdmin)


class ContentAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "title", "book_type")
    list_display_links = ("guid",)
    list_filter = ("book", "title", "book_type")
    search_fields = ["book", "title", "book_type"]
    list_editable = ("title", "book_type")


admin.site.register(Content, ContentAdmin)


class RateAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "point", "owner")
    list_display_links = ("guid",)
    list_filter = ("book", "point", "owner")
    search_fields = ["book", "point", "owner"]
    list_editable = ("point", "owner")


admin.site.register(Rate, RateAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "guid", "owner")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
    )
    search_fields = ["book", "owner"]
    list_editable = ("owner",)


admin.site.register(Review, ReviewAdmin)


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "owner")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
    )
    search_fields = ["book", "owner"]
    list_editable = ("owner",)


admin.site.register(Favourite, FavouriteAdmin)


class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "owner")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
    )
    search_fields = ["book", "owner"]
    list_editable = (
        "book",
        "owner",
    )


admin.site.register(Recommendation, RecommendationAdmin)


class ViewAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "owner")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
    )
    search_fields = ["book", "owner"]
    list_editable = (
        "book",
        "owner",
    )


admin.site.register(View, ViewAdmin)


class BookTypeAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "book_type", "price")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "book_type",
    )
    search_fields = ["book", "book_type"]
    list_editable = (
        "book",
        "book_type",
        "price",
    )


admin.site.register(BookType, BookTypeAdmin)
