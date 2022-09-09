import json

from django.db import models

import roles
#import sys
#sys.path.append("..")
from usuarios.models import Usuario
from django.apps import apps

from django.core import serializers
import itertools


class ManejoProyectos(models.Manager):

    def importarRoles(self, datos):
        idProyectoActual = datos['idProyectoActual']
        idProyectoExterno = datos['idProyectoExterno']

        # Se valida en los controllers
        proyectoActual = Proyecto.objects.get(id=idProyectoActual)
        proyectoExterno = Proyecto.objects.get(id=idProyectoExterno)
        listaRoles = apps.get_model('roles.Rol').objects.filter(proyecto=idProyectoExterno)
        listaRolesActuales = apps.get_model('roles.Rol').objects.filter(proyecto=idProyectoActual)
        listaNuevosRoles = []

        for r in listaRoles:
                rolNuevo = apps.get_model('roles.Rol').objects.crearRolInterno(nombre=r.nombre, descripcion=r.descripcion, idProyecto=proyectoActual.id)
                listaPermisosExterno = apps.get_model('roles.Rol').objects.listarPermisos(id=r.id)
                listaPermisosActual = []
                for perm in listaPermisosExterno:
                    listaPermisosActual.append({"nombre": "proyectos." + perm.codename, "idObjeto": idProyectoActual})

                # Agregamos permisos de objeto
                apps.get_model('roles.Rol').objects.agregarListaPermisoObjeto(r=rolNuevo, lista=listaPermisosActual)
                listaNuevosRoles.append(rolNuevo)

        return listaNuevosRoles


    def crearProyecto(self, datos):
        nombre = datos['nombre']
        descripcion = datos['descripcion']
        fechaInicio = datos['fechaInicio']
        fechaFin = datos['fechaFin']
        scrumMaster = Usuario.objects.get(email=datos['scrumMaster']) # Obtenemos el usuario Scrum Master por su id, que es su correo
        estado = "planificación"
        proyecto = self.model(nombre=nombre, descripcion=descripcion, fechaInicio=fechaInicio,
                              fechaFin=fechaFin, scrumMaster=scrumMaster, estado=estado)
        proyecto.save()


        return proyecto
    #TODO: Añadir fecha de inicio automáticamente cuando el SM inicie el proyecto
    #TODO: Añadir fecha de fin automáticamente cuando el SM finalice el proyecto

    def modificarProyecto(self, datos):
        proyecto = Proyecto.objects.get(id=int(datos['id']))
        proyecto.nombre = datos['nombre']
        proyecto.descripcion = datos['descripcion']
        proyecto.fechaInicio = datos['fechaInicio']
        proyecto.fechaFin = datos['fechaFin']
        proyecto.scrumMaster = Usuario.objects.get(email=datos['scrumMaster'])
        # El estado del proyecto no se modifica manualmente, sino automáticamente

        proyecto.save()
        return proyecto

    def iniciarProyecto(self, datos):
        proyecto = Proyecto.objects.get(id=int(datos['id']))
        proyecto.estado = "iniciado"

        proyecto.save()
        return proyecto





class ManejoParticipantes(models.Manager):
    def crearParticipante(self, datos):

        proyecto = Proyecto.objects.get(id=int(datos['idProyecto']))
        usuario = Usuario.objects.get(id=int(datos['idUsuario']))

        participante = self.model(proyecto=proyecto, usuario=usuario)

        participante.save()

        return participante

    def listarProyectosdeParticipante(self, id):

        listaQuery = participante.objects.filter(usuario_id=id).values("proyecto")

        print("listaQuery = ", listaQuery)
        proyectos = []
        for i in range(len(listaQuery)):
            idProyecto = listaQuery[i]['proyecto']
            proyectos.append(Proyecto.objects.get(id=int(idProyecto)))

        print("proyectosID", proyectos)

        return proyectos

    def listarParticipantedeProyectos(self, idProyecto):

        listaQuery = participante.objects.filter(proyecto=idProyecto).values("usuario")

        print("listaQuery = ", listaQuery)
        usuarios = []
        for i in range(len(listaQuery)):
            idUsuario = listaQuery[i]['usuario']
            usuarios.append(Usuario.objects.get(id=int(idUsuario)))

        print("usuarios", usuarios)

        return usuarios

    def borrarParticipante(self, datos):
        particip = participante.objects.get(id=int(datos['id_participante']))
        particip.delete()



    # Falta corregir este método para el put, no funciona
    '''
    def modificarParticipante(self, datos):
        particip = participante.objects.get(id=int(datos['idParticipante']))
        particip.proyecto = Proyecto.objects.get(id=int(datos['idProyecto']))
        #particip.usuario = Usuario.objects.get(id=int(datos['idUsuario'])) # Busca con id
        particip.usuario = Usuario.objects.get(email=datos['mailUsuario'])
        # El estado del proyecto no se modifica manualmente, sino automáticamente

        proyecto.save()
        return proyecto
    '''



class Proyecto(models.Model):
    #El id se genera de forma automática
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateTimeField(null=True) #Incluye minutos y segundos
    fechaFin = models.DateTimeField(null=True)
    scrumMaster = models.ForeignKey(Usuario, on_delete=models.PROTECT) #Evita que se borre, se soluciona cambiando de Scrum Master y luego borrando al usuario
    estado = models.CharField(max_length=30)

    objects = ManejoProyectos()
    def __str__(self):
        return str([self.nombre, self.descripcion,self.fechaInicio, self.fechaFin,
                    self.scrumMaster.id, self.estado])

    class Meta:
        #default_permissions = ()  # ?deshabilitamos add/change/delete/view

        permissions = (
            ('crear_proyecto', 'Crear un nuevo proyecto'),
            ('eliminar_proyecto', 'Eliminar un proyecto'),
            ('actualizar_proyecto', 'Actualizar los parametros iniciales de un proyecto'),
            ('archivar_proyecto', 'Archivar un proyecto'),
            ('cambiar_estado_proyecto', 'Modificar el estado de un proyecto'),
            ('listar_proyectos', 'Listar uno o varios proyectos'),
            ('iniciar_proyecto', 'Marcar un proyecto como iniciado'),
            ('crear_tipo_HU', 'Crear un nuevo tipo de Historia de Usuario'),
            ('borrar_tipo_HU', 'Borrar un tipo de HU'),
            ('importar_roles_internos', 'Importar roles internos de otro proyecto'),
            ('agregar_participante', 'Agregar un usuario a un proyecto'),
            ('modificar_participante', 'Modificar un participante'),
            ('borrar_participante', 'Borrar participante'),
            ('listar_participante', 'Lista un participante individual'),
            ('listar_roles_internos', 'Listar todos los roles internos del sistema'),
            ('crear_rol_interno', 'Crear un nuevo rol interno'),
            ('actualizar_rol_interno', 'Actualizar un rol interno'),
            ('borrar_rol_interno', 'Borrar un rol interno de proyecto'),
        )
# Participante de un proyecto (separado de usuario)
class participante(models.Model):
    # El id se genera de modo automático
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE) # Se elimina el proyecto, se eliminan sus participantes
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) # Si borramos el usuario, se borran todas sus participaciones
    #rol = models.ForeignKey(Rol_Interno, on_delete=models.PROTECT) Si borramos un rol interno, ¿qué ocurre con los usuarios que tienen ese rol?
    #TODO: Combinar modelo de participante con roles
    objects=ManejoParticipantes()
    def __str__(self):
        return str([self.proyecto, self.usuario])




