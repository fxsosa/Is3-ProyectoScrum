# Generated by Django 4.1 on 2022-09-04 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('usuarios', '0004_remove_usuario_rol'),
        ('roles', '0002_rename_rol_externo_rolexterno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, unique=True)),
                ('tipo', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=250, null=True)),
                ('rolGrupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'permissions': (('listar_roles_internos', 'Listar todos los roles internos del sistema'), ('listar_roles_externos', 'Listar todos los roles externos del sistema'), ('crear_rol_interno', 'Crear un nuevo rol interno'), ('crear_rol_externo', 'Crear nuevo rol externo'), ('actualizar_rol_interno', 'Actualizar un rol interno'), ('actualizar_rol_externo', 'Actualizar un rol externo'), ('borrar_rol_interno', 'Borrar un rol interno de proyecto'), ('borrar_rol_externo', 'Borrar un rol externo del sistema')),
                'default_permissions': (),
            },
        ),
        migrations.DeleteModel(
            name='RolExterno',
        ),
    ]