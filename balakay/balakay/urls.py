from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Balakay API",
        default_version='v1',
        description="API documentation for the Balakay project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@balakay.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('centers/', include('centers.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('analytics/', include('analytics.urls')),

]
