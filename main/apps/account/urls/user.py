from django.urls import path, include

from ..views import user
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path("login/", view=user.user_login_view, name="user_login"),
    # path("logout/", view=user.user_logout_view, name="user_logout"),
    path("list/", view=user.user_list_view, name="user_list"),
    path(
        "generate/password/",
        view=user.user_generate_password_view,
        name="user_generate_password",
    ),
    path(
        "<uuid:guid>/detail/",
        user.user_detail_api_view,
        name="user_detail",
    ),
    path(
        "<uuid:guid>/update/",
        user.user_update_api_view,
        name="user_update",
    ),

    path('register/', user.user_registration_api_view, name='register'),

    path('user-login/', user.MyObtainTokenPairView.as_view(), name='user-login'),

    path('verify-phone/', user.user_otp_verify_api_view, name='verify-phhone'),

    path('password-reset/', user.password_reset_api_view, name='password-reset'),
    path('password-reset-check/', user.password_reset_check_view, name='password-reset-check'),
    path('password-reset-confirm/', user.password_reset_confirm_view, name='password-reset-confirm'),
    path("logout/", view=user.user_logout_view, name="user_logout"),

    path("password-change/", view=user.password_change_view, name="password-change"),

    path("resend-otp/", view=user.user_resend_otp_api_view, name="password-change"),

]
