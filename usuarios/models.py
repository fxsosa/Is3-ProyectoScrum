from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from roles.models import Rol_Externo

from .manager import ManejoUsuarios
"""
Este es un comentario de prueva
"""

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nombres = models.CharField(_('user names'), max_length=80)
    apellidos = models.CharField(_('user lastnames'), max_length=80)
    rol = models.ForeignKey(Rol_Externo, on_delete=models.SET_NULL, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ManejoUsuarios()

    def __str__(self):
        return str([self.email, self.nombres, self.apellidos, self.rol.nombre if self.rol is not None else None])
