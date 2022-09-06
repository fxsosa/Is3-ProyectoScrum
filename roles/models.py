from django.db import models
from django.contrib.auth.models import Group

from proyectos.models import Proyecto
from usuarios.models import Usuario
from guardian.shortcuts import assign_perm, remove_perm

# TO-DO: Arreglar esto
permisosExternos = [
    'soportepermisos.listar_permisos',
    'roles.listar_roles_internos',
    'roles.listar_roles_externos',
    'roles.crear_rol_interno',
    'roles.crear_rol_externo',
    'roles.actualizar_rol_interno',
    'roles.actualizar_rol_externo',
    'roles.borrar_rol_interno',
    'roles.borrar_rol_externo',
    'roles.listar_permisos_externos',
    'usuarios.modificar_roles_externos_de_usuario'
]

permisosInternos = [
    'roles.listar_roles_internos', 'roles.crear_rol_interno',
    'roles.actualizar_rol_interno', 'roles.borrar_rol_interno',
]

class ManejoRol(models.Manager):


    def obtenerNombreGrupo(self, rol):
        print("aaaaaaaaaaaaaaa")
        print("rol.tipo ", rol.tipo)
        if rol.tipo == "Interno":
            print("aca no deberia")
            p = rol.proyecto
            return str(str(rol.id) + "_" + str(p.id))
        elif rol.tipo == "Externo":
            print("eeeeeeeeeeeee")
            return str(rol.id)


    def crearRolExterno(self, nombre, **extra_fields):
        """
        Crear un rol externo y registrar el modelo en la base de datos
        :param nombre: Nombre del rol a registrar
        :param extra_fields: Campos extra del modelo (descripcion)
        :return: Objeto Rol
        """

        rolExterno = self.model(nombre=nombre, tipo='Externo', rolGrupo=None, proyecto=None, **extra_fields)
        rolExterno.save()
        nombreGrupo = Rol.objects.obtenerNombreGrupo(rolExterno)
        grupo = Group.objects.create(name=nombreGrupo)
        rolExterno.rolGrupo = grupo
        rolExterno.save()

        return rolExterno

    def crearRolInterno(self, nombre, idProyecto, **extra_fields):
        """
        Crear un Rol Interno y registrar el modelo en la base de datos

        :param nombre: Nombre del rol a registrar
        :param extra_fields: Campos extra del modelo (descripcion)
        :return: Objeto Rol
        """

        try:
            proyecto = Proyecto.objects.get(id=idProyecto)
        except Proyecto.DoesNotExist as e:
            print("No existe el proyecto del rol interno a agregar!")
            return None

        rolInterno = self.model(nombre=nombre, tipo='Interno', rolGrupo=None, proyecto=proyecto, **extra_fields)
        rolInterno.save()
        nombreGrupo = Rol.objects.obtenerNombreGrupo(rolInterno)
        grupo = Group.objects.create(name=nombreGrupo)
        rolInterno.rolGrupo = grupo
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
        print("listaQuery = ",listaQuery)
        listaRoles = []
        for i in range(len(listaQuery)):
            idRol = listaQuery[i]['name']
            print("idRol ",idRol)
            try:
                nombreRol = idRol[0:idRol.index('_')]
            except:
                nombreRol = idRol
            listaRoles.append(nombreRol)
            print(listaRoles)

        return listaRoles

    def asignarRolaUsuario(self, idRol, user):
        """
        Asigna un rol a un usuario dado
        :param idRol: id del rol a asignar
        :param user: Usuario a recibir el rol
        :return: None
        """
        
        rol = Rol.objects.get(id=idRol)
        print("aquisssssssssssss")
        nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
        print(nombreGrupo + "+++++++++")
        grupo = Group.objects.get(name=nombreGrupo)
        grupo.user_set.add(user)

    def eliminarRolaUsuario(self, idRol, user):
        """
        Elimina un rol a un usuario dado
        :param idRol: id del rol a eliminar
        :param user: Usuario a eliminar el rol
        :return: None
        """

        grupo = Group.objects.get(id=idRol)
        grupo.user_set.remove(user)

    def existeRol(self, nombreRol):
        """
        Verifica si un Rol existe o no en la base de datos
        :param nombreRol: Nombre del rol a verificar
        :return: True si el objeto existe, False en caso contrario
        """

        return Rol.objects.filter(nombre=nombreRol).exists()


    def existeRolId(self, id):
        print('Probamos con get')
        try:
            rol = Rol.objects.get(id=id)
        except Rol.DoesNotExist as e:
            print("exploto")
            return False
        return True

    def agregarPermisoDeObjeto(self, idRol, nombrePermiso, nombreObjeto):
        """
        Agrega permiso a operar en el objeto dado, al Rol referenciado

        :param nombreRol: Nombre del Rol referenciado
        :param nombrePermiso: Nombre del permiso a otorgar
        :param nombreObjeto: Objeto del cual damos el permiso
        :return: None
        """

        try:
            rol = Rol.objects.get(id=idRol)
            nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
            grupo = Group.objects.get(name=nombreGrupo)
            assign_perm(nombrePermiso, grupo, nombreObjeto)
        except Rol.DoesNotExist as e:
            print("No existe el rol con id = " + idRol)

    def agregarListaPermisoDeObjeto(self, nombreRol, nombrePermiso, nombreObjeto):
        pass

    def agregarPermisoGlobal(self, idRol, nombrePermiso):
        """
        Agrega permisos globales al rol
        Estos permisos globales son similares a los permisos de clase (afectan a todas
        las instancias de una clase)

        :param nombreRol: Nombre del rol al cual asignar los permisos
        :param nombrePermiso: Nombre del permiso global a asignar
        :return: None
        """

        rol = Rol.objects.get(id=idRol)
        nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
        grupo = Group.objects.get(name=nombreGrupo)
        assign_perm(nombrePermiso, grupo)

    def agregarListaPermisoGlobal(self, r, lista):
        """
        Agrega una lista de permisos al Rol actual (self)
        :param lista: lista de json objects. Tiene el siguiente formato
        '[{"permiso":'nombre1'}, {"permiso":'nombre2'}, {"permiso":'nombre3'}]'
        :param r: Rol al cual agregar permisos
        :return: None
        """

        nombreGrupo = Rol.objects.obtenerNombreGrupo(r)
        grupo = Group.objects.get(name=nombreGrupo)
        tipo = r.tipo
        if tipo == 'Interno':
            for p in lista:
                if p in permisosInternos:
                    assign_perm(p, grupo)
        elif tipo == 'Externo':
            for p in lista:
                if p in permisosExternos:
                    assign_perm(p, grupo)

    def borrarListaPermisoGlobal(self, r, lista):
        """
        Elimina una lista de permisos al Rol actual (self)
        :param lista: lista de json objects. Tiene el siguiente formato
        '[{"permiso":'nombre1'}, {"permiso":'nombre2'}, {"permiso":'nombre3'}]'
        :param r: Rol al cual elimina permisos
        :return: None
        """

        nombreGrupo = Rol.objects.obtenerNombreGrupo(r)
        grupo = Group.objects.get(name=nombreGrupo)
        tipo = r.tipo
        if tipo == 'Interno':
            for p in lista:
                if p in permisosInternos:
                    remove_perm(p, grupo, None)
        elif tipo == 'Externo':
            for p in lista:
                if p in permisosExternos:
                    remove_perm(p, grupo, None)


    def borrarRol(self, idRol):
        """
        Borra el rol
        :param nombreRol: Nombre del rol a borrar
        :return: None
        """

        try:
            rol = Rol.objects.get(id=idRol)
            if rol.tipo == 'Interno':
                nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
                grupo = Group.objects.get(name=nombreGrupo)
                grupo.delete()
            elif rol.tipo == 'Externo':
                grupo = Group.objects.get(name=str(idRol))
                grupo.delete()

        except Rol.DoesNotExist as e:
            print("No existe el rol con id = " + idRol)
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

    def listarPermisos(self, id):
        """
        Lista todos los permisos asociados un rol
        :param nombreRol: Nombre del rol
        :return: QuerySet de permisos
        """

        try:
            rol = Rol.objects.get(id=id)
            nombreGrupo =  Rol.objects.obtenerNombreGrupo(rol)
            grupo = Group.objects.get(name=nombreGrupo)
            if grupo is not None:
                return grupo.permissions.all()
            else:
                return None
        except Rol.DoesNotExist as e:
            print("No existe rol con id = " + id)


class Rol(models.Model):
    nombre = models.CharField(max_length=50, null=True, unique=False)
    tipo = models.CharField(max_length=10, null=False)
    descripcion = models.CharField(max_length=250, null=True)
    rolGrupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)

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
            ('listar_permisos_externos', 'Para listar los permisos de un rol externo')
        )


    def __str__(self):
        return str([self.nombre])
