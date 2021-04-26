from rest_framework import routers
from django.urls import path, include
from administrador.Aplicaciones.Favs.views import *

routersFavs = routers.DefaultRouter()
routersFavs.register(r'listas', ListasViewSet)
routersFavs.register(r'favs', FavsViewSet)

urlpatterns = [
    path('Dashboard/', include(routersFavs.urls)),
]

