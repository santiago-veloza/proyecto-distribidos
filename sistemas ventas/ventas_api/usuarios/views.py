from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UsuarioSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Permite registrar sin autenticación

    @swagger_auto_schema(
        operation_description="Registra un nuevo usuario y devuelve el token JWT",
        responses={201: openapi.Response("Registro exitoso con tokens")})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            'user': UsuarioSerializer(user).data,
            'tokens': token_data
        }, status=status.HTTP_201_CREATED)


class UsuarioListView(generics.ListAPIView):
    """
    Devuelve una lista de todos los usuarios registrados (requiere autenticación).
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):  # Solo lectura
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]