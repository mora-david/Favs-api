from rest_framework import routers
from django.urls import path, include
from administrador.Aplicaciones.SSO.views import Users

routersSSO = routers.DefaultRouter()
routersSSO.register(r'', Users)

urlpatterns = [
    path('register/', include(routersSSO.urls)),
]

