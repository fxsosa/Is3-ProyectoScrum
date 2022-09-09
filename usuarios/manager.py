from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class ManejoUsuarios(BaseUserManager):
    """
    Modelo personalizado de manejo de usuarios donde el email es el PK y no el nombre
    """
    def create_user(self, email, password, username, **extra_fields):
        """
        Crear usuario con el modelo de usuario personalizado
        :param email: Email del nuevo usuario
        :param password:  Contraseña del nuevo usuario
        :param username: Username a utilizar en el sistema
        :param extra_fields: Extra_fields
        :return: Usuario
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
        Crear un superusuario con todos los permisos del sistema
        :param email: Email
        :param password: Password
        :param username: Username
        :param extra_fields: Extra_fields
        :return: Usuario
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, username,**extra_fields)

