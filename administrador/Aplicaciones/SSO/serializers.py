from rest_framework import serializers
from administrador.Aplicaciones.SSO.models import CustomUser
from django.contrib.auth.hashers import make_password


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador, de uso general, de momento su único uso es para ayudar al registro de nuevos usuarios
    """

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ('username','password','email')
