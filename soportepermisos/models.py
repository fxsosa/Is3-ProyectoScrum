from django.db import models


class SoportePermisos(models.Model):
    """
        Modelo para el soporte de permisos personalizados en las vistas/controllers del sistema
    """
    class Meta:
        managed = False  # No se tienen operaciones de manejo de tabla para este modelo
        default_permissions = ()  # deshabilitamos add/change/delete/view

        permissions = (
            ('listar_roles', 'Listar todos los roles del sistema'),
            ('listar_roles_internos', 'Listar todos los roles internos del sistema'),
            ('listar_roles_externos', 'Listar todos los roles externos del sistema'),
        )
