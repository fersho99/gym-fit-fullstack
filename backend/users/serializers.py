from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from users.models import User


class UserPublicSerializer(serializers.ModelSerializer):
    """Datos de un usuario tal como salen en las respuestas: sin contraseña."""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telefono', 'is_active', 'is_staff',
        ]


class UserSerializer(serializers.ModelSerializer):
    # Corrección 1: write_only hace que el hash nunca salga en una respuesta.
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        help_text='Requerida al crear. Si no se envía al editar, la contraseña no cambia.',
    )

    class Meta:
        model = User
        fields = UserPublicSerializer.Meta.fields + ['password']

    def validate_password(self, value):
        validate_password(value, user=self.instance)
        return value

    def validate(self, attrs):
        if self.instance is None and 'password' not in attrs:
            raise serializers.ValidationError({'password': 'Este campo es requerido al crear un usuario.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Corrección 2: la contraseña solo cambia si viene en la petición.
        # El manual le asignaba la de quien hace la petición (request.user).
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    """Registro público: solo acepta datos personales, nunca permisos."""

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'password']

    def validate(self, attrs):
        # Se valida aquí para que los validadores comparen contra email y username.
        candidato = User(**{k: v for k, v in attrs.items() if k != 'password'})
        try:
            validate_password(attrs['password'], user=candidato)
        except DjangoValidationError as error:
            raise serializers.ValidationError({'password': list(error.messages)})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenPairResponseSerializer(serializers.Serializer):
    """Solo documenta en Swagger la respuesta del login."""

    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenAccessResponseSerializer(serializers.Serializer):
    """Solo documenta en Swagger la respuesta del refresh."""

    access = serializers.CharField()
