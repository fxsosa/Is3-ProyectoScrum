from django.db import models
from django.contrib.auth.models import Group
from usuarios.models import Usuario
from guardian.shortcuts import assign_perm

# TO-DO: Arreglar esto
permisosExternos = [
    'soportepermisos.listar_permisos',
    'roles.listar_roles_internos', 'roles.listar_roles_externos',
    'roles.crear_rol_interno', 'roles.crear_rol_interno', 'roles.actualizar_rol_interno',
    'roles.actualizar_rol_interno', 'roles.borrar_rol_interno', 'roles.borrar_rol_externo',
]

permisosInternos = [
    'roles.listar_roles_internos', 'roles.crear_rol_interno',
    'roles.actualizar_rol_interno', 'roles.borrar_rol_interno',
]

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

    def listarRolesPorUsuario(self, userEmail):
        user = Usuario.objects.get(email=userEmail)
        listaQuery = Group.objects.filter(user=user).values('name')
        listaRoles = []
        for i in range(len(listaQuery)):
            listaRoles.append(listaQuery[i]['name'])

        return listaRoles

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

    def agregarListaPermisoDeObjeto(self, nombreRol, nombrePermiso, nombreObjeto):
        pass

    def agregarPermisoGlobal(self, nombreRol, nombrePermiso):
        """
        Agrega permisos globales al rol
        Estos permisos globales son similares a los permisos de clase (afectan a todas
        las instancias de una clase)

        :param nombreRol: Nombre del rol al cual asignar los permisos
        :param nombrePermiso: Nombre del permiso global a asignar
        :return: None
        """

        grupo = Group.objects.get(name=nombreRol)
        assign_perm(nombrePermiso, grupo)

    def agregarListaPermisoGlobal(self, r, lista):
        """
        Agrega una lista de permisos al Rol actual (self)
        :param lista: lista de json objects. Tiene el siguiente formato
        '[{"permiso":'nombre1'}, {"permiso":'nombre2'}, {"permiso":'nombre3'}]'
        :param r: Rol al cual agregar permisos
        :return: None
        """

        grupo = Group.objects.get(name=r.nombre)
        tipo = r.tipo
        if tipo == 'Interno':
            for p in lista:
                if p in permisosInternos:
                    assign_perm(p, grupo)
        elif tipo == 'Externo':
            for p in lista:
                if p in permisosExternos:
                    assign_perm(p, grupo)


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

    def listarPermisos(self, nombreRol):
        """
        Lista todos los permisos asociados un rol
        :param nombreRol: Nombre del rol
        :return: QuerySet de permisos
        """

        grupo = Group.objects.get(name=nombreRol)
        if grupo is not None:
            return grupo.permissions.all()
        else:
            return None


class Rol(models.Model):
    nombre = models.CharField(max_length=50, null=True, unique=True)
    tipo = models.CharField(max_length=10, null=False)
    descripcion = models.CharField(max_length=250, null=True)
    rolGrupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    objects = ManejoRol()

    class Meta:
        default_permissions = ()  # deshabilitamos add/change/delete/view

        permissions = (
            ('listar_roles_internos', 'Listar todos los roles internos del sistema'),
            ('listar_roles_externos', 'Listar todos los roles externos del sistema'),
            ('crear_rol_interno', 'Crear un nuevo rol interno'),
            ('crear_rol_externo', 'Crear nuevo rol externo'),
            ('actualizar_rol_interno', 'Actualizar un rol interno'),
            ('actualizar_rol_externo', 'Actualizar un rol externo'),
            ('borrar_rol_interno', 'Borrar un rol interno de proyecto'),
            ('borrar_rol_externo', 'Borrar un rol externo del sistema'),
        )


    def __str__(self):
        return str([self.nombre])
