from django.db import models
from django.contrib.auth.models import Group, Permission

from proyectos.models import Proyecto
from usuarios.models import Usuario
from guardian.shortcuts import assign_perm, remove_perm, get_group_perms

# TO-DO: Arreglar esto (pasar a utils)
permisosExternos = [
    'soportepermisos.listar_permisos',
    'roles.listar_roles_externos',
    'roles.crear_rol_externo',
    'roles.actualizar_rol_externo',
    'roles.borrar_rol_externo',
    'roles.listar_permisos_externos',
    'usuarios.modificar_roles_externos_de_usuario',
    'proyectos.listar_proyectos',
    'proyectos.crear_proyecto',
]

permisosInternos = [
    'proyectos.crear_proyecto',
    'proyectos.eliminar_proyecto',
    'proyectos.actualizar_proyecto',
    'proyectos.archivar_proyecto',
    'proyectos.cambiar_estado_proyecto',
    'proyectos.listar_proyectos',
    'proyectos.iniciar_proyecto',
    'proyectos.crear_tipo_HU',
    'proyectos.borrar_tipo_HU',
    'proyectos.importar_roles_internos',
    'proyectos.agregar_participante',
    'proyectos.modificar_participante',
    'proyectos.borrar_participante',
    'proyectos.listar_participante',
    'proyectos.listar_roles_internos',
    'proyectos.crear_rol_interno',
    'proyectos.actualizar_rol_interno',
    'proyectos.borrar_rol_interno',
]

class ManejoRol(models.Manager):
    """
        Manager del modelo de roles
    """

    def obtenerNombreGrupo(self, rol):
        """
        Retorna el nombre del grupo al cual pertenece un rol
        :param rol: Instancia Rol
        :return: String con el nombre del grupo asociado al rol
        """
        if rol.tipo == "Interno":
            p = rol.proyecto
            return str(str(rol.id) + "_" + str(p.id))
        elif rol.tipo == "Externo":
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

        :param idProyecto: Id del proyecto a registrar
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
        """
        Genera una lista de usuarios que se encuentran asociados a un rol
        :param nombreRol: Nombre del Rol a buscar
        :return: QuerySet de Usuario
        """

        try:
            rol = Rol.objects.get(nombre=nombreRol)
        except Rol.DoesNotExist as e:
            print("No existe el rol buscado! " + str(e))
            return None

        nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
        return Usuario.objects.filter(groups__name=nombreGrupo)

    def listarRoles(self):
        """
        Lista todos los roles registrados en la base de datos
        :return: QuerySet de todos los Roles
        """

        return Rol.objects.all()

    def listarRolesPorUsuario(self, userEmail):
        """
        Lista los roles que tiene un usuario
        :param userEmail: Email del usuario a listar sus roles
        :return: Lista de id de los Roles
        """

        user = Usuario.objects.get(email=userEmail)
        listaQuery = Group.objects.filter(user=user).values('name')
        listaRoles = []
        for i in range(len(listaQuery)):
            idRol = listaQuery[i]['name']
            print("idRol ",idRol)
            try:
                nombreRol = idRol[0:idRol.index('_')]
            except:
                nombreRol = idRol
            listaRoles.append(nombreRol)

        return listaRoles

    def listarRolesInternosPorUsuario(self, userEmail, idProyecto):
        """
        Lista los roles que tiene un usuario
        :param userEmail: Email del usuario a listar sus roles
        :return: QuerySet de Rol
        """

        user = Usuario.objects.get(email=userEmail)
        listaQuery = Group.objects.filter(user=user).values('name')
        print("listaQuery = ",listaQuery)
        listaRoles = []
        for i in range(len(listaQuery)):
            idRol = listaQuery[i]['name']
            print("idRol ",idRol)
            try:
                idRol.index('_')
            except:
                pass
            copia = idRol
            nombreRol = copia[0:idRol.index('_')]
            idProyectoAux = copia[idRol.index('_'):len(idRol)]
            print(nombreRol,"++++++++++++++++",idProyectoAux)
            if idProyectoAux != idProyecto:
               pass

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
        nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
        grupo = Group.objects.get(name=nombreGrupo)
        grupo.user_set.add(user)

    def eliminarRolaUsuario(self, idRol, user):
        """
        Elimina un rol a un usuario dado
        :param idRol: id del rol a eliminar de un usuario
        :param user: Usuario a eliminar el rol
        :return: None
        """
        try:
            rol = Rol.objects.get(id=idRol)
        except Rol.DoesNotExist as e:
            print("Rol a eliminar no existe!")
            return None

        nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
        grupo = Group.objects.get(id=nombreGrupo)
        grupo.user_set.remove(user)

    def existeRol(self, nombreRol):
        """
        Verifica si un Rol existe o no en la base de datos
        :param nombreRol: Nombre del rol a verificar
        :return: Boolean True/Existe, False/No existe
        """

        return Rol.objects.filter(nombre=nombreRol).exists()


    def existeRolId(self, id):
        """
        Verificar si un rol existe o no en la base de datos
        :param id: ID del rol a verificar
        :return: Boolean True/Existe, False/No existe
        """

        try:
            rol = Rol.objects.get(id=id)
        except Rol.DoesNotExist as e:
            print("exploto")
            return False
        return True

    def agregarPermisoDeObjeto(self, idRol, nombrePermiso, objeto):
        """
        Agrega permiso a operar en el objeto dado, al Rol referenciado

        :param idRol: ID del rol referenciado
        :param nombrePermiso: Nombre del permiso a otorgar
        :param objeto: Instancia Objeto del cual damos el permiso
        :return: None
        """

        try:
            rol = Rol.objects.get(id=idRol)
            nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
            grupo = Group.objects.get(name=nombreGrupo)
            assign_perm(nombrePermiso, grupo, obj=objeto)
        except Rol.DoesNotExist as e:
            print("No existe el rol con id = " + idRol)

    def agregarListaPermisoObjeto(self, r, lista):
        """
        Agrega la lista de permisos de objeto de un Rol
        :param r: Instancia Rol
        :param lista: Lista de permisos a agregar
                [   {"nombre": "NombrePermiso1", "idObjeto": "idObjeto1"},
                    {"nombre": "NombrePermiso2", "idObjeto": "idObjeto2"}, ...
                ]
        :return: None
        """

        nombreGrupo = Rol.objects.obtenerNombreGrupo(r)
        grupo = Group.objects.get(name=nombreGrupo)
        try:
            for per in lista:
                # Verificamos que los campos no sean null
                if per['nombre'] != "" and per['idObjeto'] is not None:
                    try:
                        idObjeto = per['idObjeto']
                        proyecto = Proyecto.objects.get(id=idObjeto)

                        if r.tipo == 'Interno':

                            print("Permiso: " + per['nombre'])
                            try:
                                assign_perm(per['nombre'], grupo, proyecto)
                            except:
                                pass
                        elif r.tipo == 'Externo':
                            if per['nombre'] in permisosExternos:
                                assign_perm(per['nombre'], grupo, proyecto)
                    except Proyecto.DoesNotExist as e:
                        print("El proyecto no existe! " + str(e))
        except Exception as e:
            print("No se pudo agregar lista de permisos + " + str(e))
            return None

    def agregarPermisoGlobal(self, idRol, nombrePermiso):
        """
        Agrega permisos globales al rol
        Estos permisos globales son similares a los permisos de clase (afectan a todas
        las instancias de una clase)

        :param idRol: Nombre del rol al cual asignar los permisos
        :param nombrePermiso: Nombre del permiso global a asignar
        :return: None
        """

        try:
            rol = Rol.objects.get(id=idRol)
        except Rol.DoesNotExist as e:
            print("No existe rol")
            return None

        nombreGrupo = Rol.objects.obtenerNombreGrupo(rol)
        grupo = Group.objects.get(name=nombreGrupo)
        assign_perm(nombrePermiso, grupo)

    def agregarListaPermisoGlobal(self, r, lista):
        """
        Agrega una lista de permisos al Rol actual (self)
        :param lista: lista de json objects. Tiene el siguiente formato
                    [{'nombre1', 'nombre2', 'nombre3']
        :param r: Instancia Rol al cual agregar permisos
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
                    print(p)
                #print(p)
        grupo.save()

    def borrarListaPermisoGlobal(self, r, lista):
        """
        Elimina una lista de permisos al Rol actual (self)
        :param lista: lista de json objects. Tiene el siguiente formato
        '[{"permiso":'nombre1'}, {"permiso":'nombre2'}, {"permiso":'nombre3'}]'
        :param r: Instancia Rol al cual elimina permisos
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

    def borrarListaPermisoObjeto(self, r, lista):
        """
        Elimina la lista de permisos de objeto de un Rol
        :param r: Instancia Rol
        :param lista: Lista de permisos a eliminar
                [   {"nombre": "NombrePermiso1", "idObjeto": "idObjeto1"},
                    {"nombre": "NombrePermiso2", "idObjeto": "idObjeto2"}, ...
                ]
        :return: None
        """

        nombreGrupo = Rol.objects.obtenerNombreGrupo(r)
        grupo = Group.objects.get(name=nombreGrupo)
        try:
            for per in lista:
                # Verificamos que los campos no sean null
                if per['nombre'] != "" and per['idObjeto'] != "":
                    try:
                        idObjeto = per['idObjeto']
                        proyecto = Proyecto.objects.get(id=idObjeto)

                        if r.tipo == 'Interno':
                            if per['nombre'] in permisosInternos:
                                remove_perm(per['nombre'], grupo, proyecto)
                        elif r.tipo == 'Externo':
                            if per['nombre'] in permisosExternos:
                                remove_perm(per['nombre'], grupo, proyecto)
                    except Proyecto.DoesNotExist as e:
                        print("El proyecto no existe! " + str(e))
        except Exception as e:
            print("No se pudo borrar lista de permisos + " + str(e))
            return None


    def borrarRol(self, idRol):
        """
        Borra el rol
        :param idRol: ID del rol a borrar
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

    def listarRolesInternos(self, idProyecto):
        """
        Lista todos los roles Internos
        :return: QuerySet de Roles Internos
        """
        if idProyecto != None:
            print("Llego muy lejooooooooooo")
            return Rol.objects.filter(tipo='Interno',proyecto=idProyecto)
        else:
            return Rol.objects.filter(tipo='Interno')

    def listarRolesExternos(self):
        """
        Lista todos los roles Externos
        :return: QuerySet de Roles Externos
        """

        return Rol.objects.filter(tipo='Externo')


    def listarPermisos(self, id):
        """
        Lista todos los permisos asociados un rol
        :param id: ID del rol
        :return: QuerySet de permisos
        """

        try:
            rol = Rol.objects.get(id=id)
            nombreGrupo =  Rol.objects.obtenerNombreGrupo(rol)
            grupo = Group.objects.get(name=nombreGrupo)
            if grupo is not None:
                if rol.tipo == 'Externo':
                    print(grupo.permissions.all())
                    return grupo.permissions.all()
                elif rol.tipo == 'Interno':
                    lista = get_group_perms(grupo, rol.proyecto)
                    print(lista)
                    listaPermisos = []
                    for p in lista:
                        print(p)
                        listaPermisos.append(Permission.objects.get(codename=p))
                    return listaPermisos
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
            ('listar_roles_externos', 'Listar todos los roles externos del sistema'),
            ('crear_rol_externo', 'Crear nuevo rol externo'),
            ('actualizar_rol_externo', 'Actualizar un rol externo'),
            ('borrar_rol_externo', 'Borrar un rol externo del sistema'),
            ('listar_permisos_externos', 'Para listar los permisos de un rol externo')
        )


    def __str__(self):
        return str([self.nombre, self.tipo, self.descripcion, self.proyecto.id if self.tipo == 'Interno' else None])
