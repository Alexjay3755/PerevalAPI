from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Rest API для сайта Федерации спортивного туризма России',
        default_version='v1',
        description='Методы создания, получения и редактирования отчётов туристов о преодолении горных перевалов',
        license=openapi.License(name='pereval.online'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path( r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]