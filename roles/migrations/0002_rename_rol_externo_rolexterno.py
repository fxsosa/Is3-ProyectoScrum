# Generated by Django 4.1 on 2022-08-19 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_rol'),
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rol_Externo',
            new_name='RolExterno',
        ),
    ]