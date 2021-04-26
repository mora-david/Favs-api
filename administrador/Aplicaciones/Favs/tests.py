from django.test import TestCase
from administrador.Aplicaciones.Favs.models import *
from administrador.Aplicaciones.SSO.models import CustomUser

from rest_framework_simplejwt.tokens import RefreshToken

class FavoritosTests(TestCase):
    url = '/Dashboard/favs/'

    def test_postFav(self):
        """
        Test para crear un nuevo favorito
        """

        usuario = CustomUser.objects.create(username='pabloLopez', password="123abc")
        token = RefreshToken.for_user(usuario)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token.access_token),
            'content_type': 'application/json'
        }
        data = {'titulo':'favorito1','categorias':'video, documentacion','descripcion':'video explicativo','enlace':'https://www.google.com'}
        r = self.client.post(self.url, data, **self.headers)
        self.assertEqual(r.status_code, 201)

class ListasTests(TestCase):
    url = '/Dashboard/listas/'

    def utilCreateLista(self, val, user):
        """
        Utilidad para crear varias listas y asignarselas a un usuario
        """
        year = 2010
        for v in range(val):
            Lista.objects.create(titulo='Lista '+str(v),descripcion='esta es una breve descipción ' + str(v), created=str(year)+'-01-01', owner=user)
            year = year + 1

    def test_getListas(self):
        """
        Test para verificar que todas las listas creadas se pueden ver en JSON de respuesta de la vista
        """
        usuario = CustomUser.objects.create(username='pabloLopez',password="123abc")
        token = RefreshToken.for_user(usuario)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token.access_token),
            'content_type': 'application/json'
        }
        self.utilCreateLista(5, usuario)
        r = self.client.get(self.url,**self.headers)
        self.assertEqual(r.status_code,200)
        self.assertEqual(len(r.data),5)

    def test_postLista(self):
        """
        Test para crear una lista nueva, de inicio la lista se crea sin favoritos
        """
        usuario = CustomUser.objects.create(username='pabloLopez', password="123abc")

        data = {'titulo':'mi lista personalizada','descripcion':'esta es una breve descipción','favoritos':[ ]}


        r = self.client.post(self.url, data)
        self.assertEqual(r.status_code, 401)

        token = RefreshToken.for_user(usuario)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token.access_token),
            'content_type': 'application/json'
        }

        r = self.client.post(self.url, data, **self.headers)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['titulo'], 'mi lista personalizada')


    def test_updateFavtoList(self):
        """
        Esta lista hace un update a la lista para añadir los favoritos que se quieran
        """
        usuario = CustomUser.objects.create(username='pabloLopez', password="123abc")
        token = RefreshToken.for_user(usuario)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token.access_token),
            'content_type': 'application/json'
        }
        self.utilCreateLista(1, usuario)

        data = {'titulo': 'favorito1', 'categorias': 'video, documentacion', 'descripcion': 'video explicativo',
                'enlace': 'https://www.google.com'}
        rfav = self.client.post('/Dashboard/favs/', data, **self.headers)
        rfav = self.client.post('/Dashboard/favs/', data, **self.headers)

        data1 = {'titulo': 'mi lista personalizada', 'descripcion': 'esta es una breve descipción', 'favoritos': [1,2]}

        r = self.client.put(self.url+'1/', data1,**self.headers)
        self.assertEqual(r.status_code,200)


    def test_retrieveListandFavs(self):
        """
        Este test regresa una lista con todos los favoritos que la componen, así como la información de dichos favoritos
        """
        usuario = CustomUser.objects.create(username='pabloLopez', password="123abc")
        token = RefreshToken.for_user(usuario)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token.access_token),
            'content_type': 'application/json'
        }
        self.utilCreateLista(3, usuario)
        lista1 = Lista.objects.first()
        lista3 = Lista.objects.last()

        data = {'titulo': 'favorito1', 'categorias': 'video, documentacion', 'descripcion': 'video explicativo',
                'enlace': 'https://www.google.com'}
        rfav = self.client.post('/Dashboard/favs/', data, **self.headers)

        data1 = {'titulo': 'mi lista personalizada', 'descripcion': 'esta es una breve descipción', 'favoritos': [1]}

        r = self.client.put(self.url + '1/', data1, **self.headers)
        self.assertEqual(r.status_code, 200)

        r = self.client.get(self.url + '1/', **self.headers)
        self.assert_(r.data['favoritos'][0]['titulo'])
        self.assertEqual(r.status_code,200)

    def test_retrieveFilteredFavs(self):
        """
        Este test regresa una lista con todos los favoritos que cumplen con los filtros descritos en el path
        por ejemplo: '1/filtered/all&video&tutorial&pruebas/' regresa todos los favoritos que se encuentran en la
        lista 1 y que tienen asignadas las categorías video Y tutorial Y pruebas.
        """
        favsURL = '/Dashboard/favs/'

        usuario = CustomUser.objects.create(username='pabloLopez', password="123abc")
        token = RefreshToken.for_user(usuario)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token.access_token),
            'content_type': 'application/json'
        }
        self.utilCreateLista(1, usuario)

        #Creación de favoritos
        data = {'titulo': 'favorito1', 'categorias': 'video, documentacion', 'descripcion': 'video explicativo',
                'enlace': 'https://www.google.com'}
        r = self.client.post(favsURL, data, **self.headers)
        self.assertEqual(r.status_code, 201)

        data = {'titulo': 'favorito2', 'categorias': 'video, documentacion, tutorial', 'descripcion': 'video explicativo',
                'enlace': 'https://www.google.com'}
        r = self.client.post(favsURL, data, **self.headers)
        self.assertEqual(r.status_code, 201)

        data = {'titulo': 'favorito3', 'categorias': 'tutorial, documentacion', 'descripcion': 'video explicativo',
                'enlace': 'https://www.google.com'}
        r = self.client.post(favsURL, data, **self.headers)
        self.assertEqual(r.status_code, 201)

        # Agregando Favoritos a la lista
        data1 = {'titulo': 'mi lista personalizada', 'descripcion': 'esta es una breve descipción', 'favoritos': [1,2,3]}
        r = self.client.put(self.url + '1/', data1, **self.headers)
        self.assertEqual(r.status_code, 200)

        # Edición de fechas en favoritos para hacer test de filtro
        fav1 = Favoritos.objects.get(pk=1)
        fav1.created = 2010
        fav2 = Favoritos.objects.get(pk=2)
        fav1.created = 2015
        fav3 = Favoritos.objects.get(pk=3)
        fav1.created = 2020

        r = self.client.get(self.url + '1/filtered/all&video&tutorial/', **self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data['favoritos']), 1)

        r = self.client.get(self.url + '1/filtered/all&video&tutorial&pruebas/', **self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data['favoritos']), 0)

        r = self.client.get(self.url + '1/filtered/all&documentacion/', **self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data['favoritos']), 3)

