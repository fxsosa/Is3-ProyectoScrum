from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from roles.models import Rol


class ManejoSoportePermisos(models.Manager):

    def listarPermisos(self):
        """
        Lista los permisos del modelo soportepermisos
        :return: QuerySet, objetos Permission
        """
        content_type = ContentType.objects.get_for_model(SoportePermisos)
        listaPermisos = Permission.objects.filter(content_type=content_type)
        return listaPermisos

    def listarPermisosRolExterno(self):
        """
        Retorna una lista de permisos de modelo de rol externo
        :return: QuerySet de lista de permisos
        """

        content_type = ContentType.objects.get_for_model(Rol)
        listaPermisos = Permission.objects.filter(content_type=content_type)
        listaPermisos = listaPermisos.exclude(codename__icontains='interno')
        return listaPermisos

    def listarPermisosRolInterno(self):
        """
        Retorna una lista de permisos de modelo de rol interno
        :return: QuerySet de lista de permisos
        """

        content_type = ContentType.objects.get_for_model(Rol)
        listaPermisos = Permission.objects.filter(content_type=content_type)
        listaPermisos = listaPermisos.exclude(codename__icontains='externo')
        return listaPermisos


class SoportePermisos(models.Model):
    """
        Modelo para el soporte de permisos personalizados en las vistas/controllers del sistema
    """

    objects = ManejoSoportePermisos()

    class Meta:
        managed = False  # No se tienen operaciones de manejo de tabla para este modelo
        default_permissions = ()  # deshabilitamos add/change/delete/view

        permissions = (
            ('listar_permisos', 'Listar/ver permisos del sistema'),
        )
