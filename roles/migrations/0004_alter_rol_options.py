# Generated by Django 4.1 on 2022-09-09 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0003_rol_delete_rolexterno'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rol',
            options={'default_permissions': (), 'permissions': (('listar_roles_externos', 'Listar todos los roles externos del sistema'), ('crear_rol_externo', 'Crear nuevo rol externo'), ('actualizar_rol_externo', 'Actualizar un rol externo'), ('borrar_rol_externo', 'Borrar un rol externo del sistema'), ('listar_permisos_externos', 'Para listar los permisos de un rol externo'))},
        ),
    ]
