# Generated by Django 4.1 on 2022-08-22 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=80, null=True, verbose_name='username'),
        ),
    ]