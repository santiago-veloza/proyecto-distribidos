"""
URL configuration for ventas_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from usuarios.views import RegisterView
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny



# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API del Sistema de Ventas",
        default_version='v1',
        description="Documentación de la API del sistema de ventas",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="santiago@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

@swagger_auto_schema(method='post', tags=["token"])
@api_view(['POST'])
def custom_token_obtain_pair(request, *args, **kwargs):
    return TokenObtainPairView.as_view()(request, *args, **kwargs)

@swagger_auto_schema(method='post', tags=["token"])
@api_view(['POST'])

def custom_token_refresh(request, *args, **kwargs):
    return TokenRefreshView.as_view()(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/productos/', include('productos.urls')),
    path('api/ventas/', include('ventas.urls')),
    path('register/', RegisterView.as_view(), name='register'),

    # Rutas Swagger y Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/token/', custom_token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', custom_token_refresh, name='token_refresh'),


]
