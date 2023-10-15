"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


# swagger_schema_view = get_swagger_view(title="Book E-commerce platform")

schema_view = get_schema_view(
    openapi.Info(
    title="Swagger Doc for Liber",
    default_version='v1',
    description="This is Zukko project API",
    terms_of_service="zukko.uz",
    contact=openapi.Contact(email="burixonzoda.nusratullo@gmail.com"),
    ),
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
    public=True,
    # patterns=public_apis,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("main.apps.v1"), name="main"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path(r"", swagger_schema_view),
    path(
        "", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui-v1"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
