from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class ManejoUsuarios(BaseUserManager):
    """
    Modelo personalizado de manejo de usuarios donde el email es el PK y no el nombre
    """
    def create_user(self, email, password, username, **extra_fields):
        """
        Crear y guardar un usuario con un email y contraseña dada.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, username,**extra_fields)

