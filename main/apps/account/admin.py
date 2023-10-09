from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models.audio_book import AudioBook
from .models.balance import Balance
from .models.online_book import OnlineBook
from .models.user_book import UserBook
from .models.user import User


class BalanceTabularAdmin(admin.TabularInline):
    model = Balance


class UserAdmin(BaseUserAdmin):
    list_display = (
        "guid",
        # "phone_number",
        # "email",
        "expiration_time_register",
        "expiration_time_reset",
        "profile_picture",
        "first_name",
        # "last_name",
        "is_staff",
        "date_of_birth",
        "gender",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "profile_picture",
                    "expiration_time_register",
                    "expiration_time_reset",
                    # "first_name",
                    "first_name",
                    # "last_name",
                    # "email",
                    "date_of_birth",
                    "gender",
                    "otp",
                    "is_virified",
                    "activating_code",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_moderator",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                )
            },
        ),
    )
    search_fields = ("username",)
    inlines = [BalanceTabularAdmin]
    ordering = ("first_name",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ("guid", "amount", "owner")
    list_display_links = ("guid",)
    list_filter = (
        "amount",
        "owner",
    )
    search_fields = ("owner__first_name",)
    list_editable = (
        "amount",
        "owner",
    )


admin.site.register(Balance, BalanceAdmin)


class OnlineBookAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "owner", "state", "book_type")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
        "book_type",
    )
    search_fields = ["book__title", "state"]
    list_editable = ("book_type", "state")


admin.site.register(OnlineBook, OnlineBookAdmin)


class AudioBookAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "owner", "state", "book_type")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
        "book_type",
    )
    search_fields = ["book__title", "state"]
    list_editable = ("book_type", "state")


admin.site.register(AudioBook, AudioBookAdmin)


class UserBookAdmin(admin.ModelAdmin):
    list_display = ("guid", "book", "owner", "state", "book_type")
    list_display_links = ("guid",)
    list_filter = (
        "book",
        "owner",
        "book_type",
    )
    search_fields = ["book__title", "state"]
    list_editable = ("book_type", "state")


admin.site.register(UserBook, UserBookAdmin)
