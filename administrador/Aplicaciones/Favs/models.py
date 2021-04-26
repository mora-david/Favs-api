from django.db import models
from django.utils import timezone
from administrador.Aplicaciones.SSO.models import CustomUser

# Create your models here.


class Categorias(models.Model):
    """
    En este modelo se guardan las categorías que más adelante serán utilizadas
    para clasificar los Favoritos
    """
    categoria = models.CharField(max_length=20)

    def __str__(self):
        return self.categoria

class Favoritos(models.Model):
    """
    El modelo Favoritos guarda la información que el usuario desea guardar sobre un sitio
    web, los datos que se pedirá que ingrese el usuario son:
    - titulo
    - descripción
    - enlace
    - categorías

    El campo de owner y created se llenarán de formá automática, el campo owner mediante
    request.user y created se autogenera
    """
    titulo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)
    enlace = models.CharField(max_length=200)
    categorias = models.ManyToManyField(Categorias)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now())

class Lista(models.Model):
    """
    Este modelo contiene la clasificación de las listas, cada lista tiene sus favoritos adentro
    un ejemplo de su uso, es la lista "python threads", la cual puede tener varios favoritos sobre
    el tema, se agrega el campo de descripción.

    los campos que se llenan automáticamente son:
    - owener
    - created

    """
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150)
    favoritos = models.ManyToManyField(Favoritos, blank=True, related_name='favs')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now())




