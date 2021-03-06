from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from administrador.Aplicaciones.SSO.serializers import UsuarioSerializer
from administrador.Aplicaciones.SSO.models import CustomUser
from rest_framework.permissions import AllowAny


# Create your views here.


class Users(ModelViewSet):
    """
    Esta vista tiene el proposito de registrar usuarios de momento
    """
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UsuarioSerializer
    http_method_names = ['post']

