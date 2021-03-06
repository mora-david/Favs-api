from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from administrador.Aplicaciones.Favs.serializers import *
from administrador.Aplicaciones.Favs.models import *
from rest_framework.decorators import action

import copy


class ListasViewSet(ModelViewSet):
    """
    Vista que acepta los métodos:
    GET - > Regresa todos las listas solicitados por request.user (requiere que el usuario esté auténticado)
    POST - > Crea una nueva lista y la asigna al request.user (requiere que el usuario esté auténticado)
    PUT -> Permite editar valores de la lista, y se utiliza para añadir nuevos favoritos
    DETLETE -> Permite eliminar una lista y toda su información

    @action filtered -> Dado el pk de una lista, permite filtrar categorías de los favoritos, de esta manera solo
    regresará los favoritos que cumplen con el criterio de los filtros de categorías
    """
    queryset = Lista.objects.all()
    serializer_class = ListaSerializerGET
    http_method_names = ['get','post','put','delete']

    def list(self, request, *args, **kwargs):
        queryset = Lista.objects.filter(owner=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        req = copy.deepcopy(request.data)
        user = request.user
        req['owner'] = user.id
        serializer = ListaSerializer(data=req)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        req = copy.deepcopy(request.data)
        req['owner'] = request.user.id
        serializer = ListaSerializer(instance, data=req, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='filtered/(.*)')
    def filtered(self, request, pk=None):
        filtros = request.get_full_path()[29:-1].split('&')
        serializer = ListaSerializerFiltered(self.get_object(), many=False, context={'categorias':filtros[1:]})
        return Response(serializer.data)


class FavsViewSet(ModelViewSet):
    """
    Esta vista permite los siguientes verbos http
    POST -> Crea un nuevo Favorito
    UPDATE -> Permite actualizar información del favorito
    DELETE -> Permite eliminar un favorito

    De momento no permite GET, ya que los favoritos se visualizan a través del retrieve de la lista a la que están
    asignados
    """
    queryset = Favoritos.objects.all()
    serializer_class = FavsSerializerGet
    http_method_names = ['post','put','delete']

    def create(self, request, *args, **kwargs):
        req = copy.deepcopy(request.data)
        user = request.user
        req['owner'] = user.id
        categorias = req['categorias'].split(', ')

        cats = []
        for c in categorias:
            cat1 = Categorias.objects.filter(categoria=c)
            if not cat1:
                cat = Categorias.objects.create(categoria=c)
                cats.append(str(cat.id))
            else:
                cats.append(str(cat1[0].id))

        req['categorias'] = cats

        serializer = FavsSerializer(data=req)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



