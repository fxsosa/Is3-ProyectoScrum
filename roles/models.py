from django.db import models
from django.contrib.auth.models import Group
from usuarios.models import Usuario
from guardian.shortcuts import assign_perm


class ManejoRol(models.Manager):

    def crearRolExterno(self, nombre, **extra_fields):
        """
        Crear un rol externo y registrar el modelo en la base de datos
        :param nombre: Nombre del rol a registrar
        :param extra_fields: Campos extra del modelo (descripcion)
        :return: Objeto Rol
        """

        grupo = Group.objects.create(name=nombre)
        rolExterno = self.model(nombre=nombre, tipo='Externo', rolGrupo=grupo, **extra_fields)
        rolExterno.save()
        return rolExterno

    def crearRolInterno(self, nombre, **extra_fields):
        """
        Crear un Rol Interno y registrar el modelo en la base de datos

        :param nombre: Nombre del rol a registrar
        :param extra_fields: Campos extra del modelo (descripcion)
        :return: Objeto Rol
        """

        grupo = Group.objects.create(name=nombre)
        rolInterno = self.model(nombre=nombre, tipo='Interno', rolGrupo=grupo, **extra_fields)
        rolInterno.save()
        return rolInterno

    def listarUsuarios(self, nombreRol):
        return Usuario.objects.filter(groups__name=nombreRol)

    def listarRoles(self):
        """
        Lista todos los roles registrados en la base de datos
        :return: QuerySet de todos los Roles
        """

        return Rol.objects.all()

    def asignarRolaUsuario(self, nombreRol, user):
        """
        Asigna un rol a un usuario dado
        :param nombreRol: Nombre del rol a asignar
        :param user: Usuario a recibir el rol
        :return: None
        """

        grupo = Group.objects.get(name=nombreRol)
        grupo.user_set.add(user)

    def existeRol(self, nombreRol):
        """
        Verifica si un Rol existe o no en la base de datos
        :param nombreRol: Nombre del rol a verificar
        :return: True si el objeto existe, False en caso contrario
        """

        return Rol.objects.filter(nombre=nombreRol).exists()

    def agregarPermisoDeObjeto(self, nombreRol, nombrePermiso, nombreObjeto):
        """
        Agrega permiso a operar en el objeto dado, al Rol referenciado

        :param nombreRol: Nombre del Rol referenciado
        :param nombrePermiso: Nombre del permiso a otorgar
        :param nombreObjeto: Objeto del cual damos el permiso
        :return: None
        """

        grupo = Group.objects.get(name=nombreRol)
        assign_perm(nombrePermiso, grupo, nombreObjeto)

    def agregarPermisoGlobal(self, nombreRol, nombrePermiso):
        """
        Agrega permisos globales al rol
        Estos permisos globales son similares a los permisos de clase (afectan a todas
        las instancias de una clase)

        :param nombreRol: Nombre del rol al cual asignar los permisos
        :param nombrePermiso: Nombre del permiso global a asignar
        :return: None
        """

        grupo = Group.objects.get(nombre=nombreRol)
        assign_perm(nombrePermiso, grupo)

    def borrarRol(self, nombreRol):
        """
        Borra el rol
        :param nombreRol: Nombre del rol a borrar
        :return: None
        """

        grupo = Group.objects.get(name=nombreRol)
        grupo.delete()

    def listarRolesInternos(self):
        """
        Lista todos los roles Internos
        :return: QuerySet de Roles Internos
        """

        return Rol.objects.filter(tipo='Interno')

    def listarRolesExternos(self):
        """
        Lista todos los roles Externos
        :return: QuerySet de Roles Externos
        """

        return Rol.objects.filter(tipo='Externo')

    def actualizarRol(self, campos):
        # To do
        pass

class Rol(models.Model):
    nombre = models.CharField(max_length=50, null=True, unique=True)
    tipo = models.CharField(max_length=10, null=False)
    descripcion = models.CharField(max_length=250, null=True)
    rolGrupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    objects = ManejoRol()

    def __str__(self):
        return str([self.nombre])
