from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User
from users.serializers import (
    RegisterUserSerializer,
    TokenAccessResponseSerializer,
    TokenPairResponseSerializer,
    UserPublicSerializer,
    UserSerializer,
)


# La contraseña se maneja en UserSerializer, así aplica por igual a POST, PUT y
# PATCH (el manual solo contemplaba POST y PATCH). Los decoradores hacen que
# Swagger documente respuestas sin contraseña, igual que las que da la API.
@method_decorator(name='list', decorator=swagger_auto_schema(responses={200: UserPublicSerializer(many=True)}))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(responses={200: UserPublicSerializer}))
@method_decorator(name='create', decorator=swagger_auto_schema(responses={201: UserPublicSerializer}))
@method_decorator(name='update', decorator=swagger_auto_schema(responses={200: UserPublicSerializer}))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(responses={200: UserPublicSerializer}))
class UserApiViewSet(ModelViewSet):
    """CRUD de usuarios, solo para administradores."""

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')


class UserView(APIView):
    """Datos personales del usuario dueño del token."""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserPublicSerializer})
    def get(self, request):
        return Response(UserPublicSerializer(request.user).data)


class RegisterUserView(CreateAPIView):
    """Crea una cuenta nueva; no requiere iniciar sesión."""

    permission_classes = [AllowAny]
    # Sin autenticación, un token vencido no bloquea el registro.
    authentication_classes = []
    serializer_class = RegisterUserSerializer


# Sin estas subclases, Swagger documenta que el login responde con el email y
# la contraseña, cuando en realidad responde con los tokens.
class LoginView(TokenObtainPairView):
    """Recibe email y contraseña; devuelve los tokens de acceso y de refresh."""

    @swagger_auto_schema(responses={200: TokenPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    """Recibe un token de refresh; devuelve un token de acceso nuevo."""

    @swagger_auto_schema(responses={200: TokenAccessResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
