from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['rol']

class UsuarioSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance = super().update(instance, validated_data)

        if profile_data:
            # Actualiza el perfil asociado
            Profile.objects.filter(user=instance).update(**profile_data)

        return instance
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    rol = serializers.CharField(write_only=True)  # ❗ obligatorio ahora

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'rol']

    def create(self, validated_data):
        rol = validated_data.pop('rol')  # Se extrae el rol ingresado
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Crear el perfil con el rol proporcionado
        Profile.objects.create(user=user, rol=rol)

        return user
