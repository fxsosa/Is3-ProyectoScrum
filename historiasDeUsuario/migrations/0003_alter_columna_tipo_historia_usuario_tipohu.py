# Generated by Django 4.1 on 2022-09-09 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('historiasDeUsuario', '0002_rename_proyect_tipo_historia_usuario_proyectos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columna_tipo_historia_usuario',
            name='tipoHU',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historiasDeUsuario.tipo_historia_usuario'),
        ),
    ]
