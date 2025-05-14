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
from usuarios.views import RegisterView, UsuarioListView
#from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
#from rest_framework.permissions import AllowAny



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

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=["token"],  # Aquí forzamos que el grupo se llame "token"
        operation_summary="Obtener token JWT",
        operation_description="Obtiene un par de tokens (access y refresh) para el usuario autenticado.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=["token"],
        operation_summary="Refrescar token JWT",
        operation_description="Recibe un refresh token y devuelve un nuevo access token.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/productos/', include('productos.urls')),
    path('api/ventas/', include('ventas.urls')),
    path ('usuarios/', include('usuarios.urls')),

    path('register/', RegisterView.as_view(), name='register'),
    

    # Rutas Swagger y Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

]
