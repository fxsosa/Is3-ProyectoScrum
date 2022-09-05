from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import ManejoUsuarios
"""
Este es un comentario de prueva
"""

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=80, null=True)
    nombres = models.CharField(_('user names'), max_length=80)
    apellidos = models.CharField(_('user lastnames'), max_length=80)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ManejoUsuarios()

    def __str__(self):
        return str([self.email, self.username, self.nombres, self.apellidos])

    class Meta:

        permissions = (
            ('modificar_roles_externos_de_usuario', 'Permiso para el administrador de editar roles externos'),
        )