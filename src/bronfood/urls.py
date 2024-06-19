from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from bronfood.api.views import CustomTokenCreateView, healthcheck

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck/', healthcheck),  # noqa
    path('api/', include('bronfood.api.urls')),
    path('client/', include('bronfood.api.client.urls', namespace='client')),
    path('signin/', CustomTokenCreateView.as_view(), name="signin"),
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

schema_view = get_schema_view(
    openapi.Info(
        title="bronfood.com API",
        default_version="v1",
        description="Документация для проекта bronfood.com",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="admin@bronfood.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]
