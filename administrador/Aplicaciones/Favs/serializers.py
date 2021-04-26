from rest_framework import serializers
from administrador.Aplicaciones.Favs.models import *
from django.db.models.expressions import RawSQL


class CatSerializer(serializers.ModelSerializer):
    """
    El serializer regresa las categorías que contiene un favorito, solo es utilizado como complemento
    para el serializador FavSerializerGet
    """
    class Meta:
        model = Categorias
        fields = ('categoria',)


class FavsSerializerGet(serializers.ModelSerializer):
    """
    El serializador de momento tiene la función de regresar todos los favoritos de una lista en el list de dicha lista
    """
    categorias = CatSerializer(many=True)

    class Meta:
        model = Favoritos
        fields = ('titulo', 'descripcion', 'enlace', 'categorias', 'owner','id')


class FavsSerializer(serializers.ModelSerializer):
    """
    El serializador es de uso general más concreatamente para el método create de los favoritos.
    """
    class Meta:
        model = Favoritos
        fields = ('titulo', 'descripcion', 'enlace', 'categorias', 'owner','id')


class ListaSerializer(serializers.ModelSerializer):
    """
    Serializador utilizado para los métodos create y update, principalmente para crear nuevas listas y agregar
    nuevos favoritos mediante put.
    """
    class Meta:
        model = Lista
        fields = '__all__'


class ListaSerializerGET(serializers.ModelSerializer):
    """
    Este serializador tiene el propósito de regresar todas las listas del usuario que hace request, regresa
    también los favoritos de dichas listas.
    """
    favoritos = FavsSerializerGet(many=True)

    class Meta:
        model = Lista
        fields = '__all__'


class ListaSerializerFiltered(serializers.ModelSerializer):
    """
    Este serializador tiene el propósito de regresar todas las listas del usuario que hace request, regresa
    también los favoritos de dichas listas, este serializer trabaja con un action en la viewset, que le permite
    con base a las categorías solicitadas por el path regresar solo los favoritos que cumplan con los criterios de las
    categorías.
    """
    favoritos = serializers.SerializerMethodField()

    class Meta:
        model = Lista
        fields = '__all__'

    def get_favoritos(self, obj):
        fav1 = Favoritos.objects.filter(favs__id=obj.id)

        cat = self.context.get("categorias")
        for v, x in enumerate(cat):
            q = fav1.filter(categorias=RawSQL("select id from Favs_categorias where categoria = %s",[x])) if v == 0 \
                else q.filter(categorias=RawSQL("select id from Favs_categorias where categoria = %s", [x]))

        serializer = FavsSerializerGet(instance=q, many=True)

        return serializer.data
