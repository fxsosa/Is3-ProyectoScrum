from django.db import models
#import sys
#sys.path.append("..")
from usuarios.models import Usuario

class ManejoParticipantes(models.Manager):
    def listarProyectosdeParticipante(self, id):

        proyectos = Participante.objects.filter(idProyecto__participante=id)

        if len(proyectos) == 0:
            return proyectos

        proyectos = proyectos.values_list('idProyecto')
        return proyectos




class ManejoProyectos(models.Manager):

    def crearProyecto(self, datos):
        nombre = datos['nombre']
        descripcion = datos['descripcion']
        fechaInicio = datos['fechaInicio']
        fechaFin = datos['fechaFin']
        scrumMaster = Usuario.objects.get(email=datos['scrumMaster'])
        #scrumMaster = datos['scrumMaster']
        estado = datos['estado']
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
        proyecto.estado = datos['estado']

        proyecto.save()
        return proyecto

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
            ('cambiar_estado_proyecto', 'Modificar el estado de un proyecto')
        )
# Participante de un proyecto (separado de usuario)
class Participante(models.Model):
    # El id se genera de modo automático
    idProyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE) # Se elimina el proyecto, se eliminan sus participantes
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) # Si borramos el usuario, se borran todas sus participaciones
    #rol = models.ForeignKey(Rol_Interno, on_delete=models.PROTECT) Si borramos un rol interno, ¿qué ocurre con los usuarios que tienen ese rol?
    #TODO: Combinar modelo de participante con roles
    def __str__(self):
        return str([self.idProyecto, self.idUsuario])

    objects = ManejoParticipantes()