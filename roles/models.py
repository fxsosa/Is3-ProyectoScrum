from django.db import models
from django.contrib.auth.models import Group
from usuarios.models import Usuario


class ManejoRol(models.Manager):

    def crearRolExterno(self, nombre, **extra_fields):
        grupo = Group.objects.create(name=nombre)
        rolExterno = self.model(nombre=nombre, tipo='Externo', rolGrupo=grupo, **extra_fields)
        rolExterno.save()
        return rolExterno

    def crearRolInterno(self, nombre, **extra_fields):
        grupo = Group.objects.create(name=nombre)
        rolInterno = self.model(nombre=nombre, tipo='Interno', rolGrupo=grupo, **extra_fields)
        rolInterno.save()
        return rolInterno

    def listarUsuarios(self, nombreRol):
        return Usuario.objects.filter(groups__name=nombreRol)

    def listarRoles(self):
        return Rol.objects.all()

    def asignarRol(self, nombreRol, user):
        grupo = Group.objects.get(name=nombreRol)
        grupo.user_set.add(user)

    def existeRol(self, nombreRol):
        return Rol.objects.filter(nombre=nombreRol).exists()


class Rol(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    tipo = models.CharField(max_length=10, null=False)
    descripcion = models.CharField(max_length=250, null=True)
    rolGrupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    objects = ManejoRol()

    def __str__(self):
        return str([self.nombre])
