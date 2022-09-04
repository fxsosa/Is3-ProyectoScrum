from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ManejoSoportePermisos(models.Manager):

    def listarPermisos(self):
        """
        Lista los permisos del modelo soportepermisos
        :return: QuerySet, objetos Permission
        """
        content_type = ContentType.objects.get_for_model(SoportePermisos)
        listaPermisos = Permission.objects.filter(content_type=content_type)
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
            ('listar_roles', 'Listar los roles del sistema'),
            ('listar_roles_internos', 'Listar todos los roles internos del sistema'),
            ('listar_roles_externos', 'Listar todos los roles externos del sistema'),
            ('crear_rol_interno', 'Crear un nuevo rol interno'),
            ('crear_rol_externo', 'Crear nuevo rol externo'),
            ('actualizar_rol_interno', 'Actualizar un rol interno'),
            ('actualizar_rol_externo', 'Actualizar un rol externo'),
        )
