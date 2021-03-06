from django.test import TestCase

from administrador.Aplicaciones.SSO.models import *
from django.contrib.auth.hashers import make_password


class SSO(TestCase):
    url = '/register/'
    tokenurl = '/api/token/'

    def test_postRegister(self):
        """
        Este test compueba que el usuario nuevo sea creado correctamente
        """
        data = {'username':'joseperez','email':'jose@gmail.com','password':'123abc'}
        r = self.client.post(self.url, data)
        self.assertEqual(r.status_code, 201)

    def test_getJwtToken(self):
        """
        Este test nos ayuda a verificar que la url para login nos regrese un access token y refresh token,
        de acuerdo a si el usuario está previamente registrado, ya que estos tokens son la manera de auténticarse
        en la aplicación
        """
        CustomUser.objects.create(username='joseperez',password=make_password('123abc'))
        data = {'username':'joseperez', 'password':'123abc'}
        r = self.client.post(self.tokenurl, data)
        self.assertEqual(r.status_code, 200)
        self.assert_(r.data['access'])
        self.assert_(r.data['refresh'])






