from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    """
    Este modelo de momento es igual que el abstract user, pero al definirlo aqui, se facilita la posibilidad
    de editarlo en un futuro según los requerimientos del momento
    """
    pass