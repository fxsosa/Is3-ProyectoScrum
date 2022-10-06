from django.db import models

from proyectos.models import Proyecto
from usuarios.models import Usuario
from historiasDeUsuario_proyecto.models import historiaUsuario

class ManagerSprint(models.Manager):

    def crearSprint(self, datos):
        """Crea una historia de usuario

        :param datos: Diccionario (o JSON) con los siguientes valores "key":
        nombre, descripcion, idProyecto, fechaInicio, fechaFin, capacidadEquipo, estado.

        :return: QuerySet de Sprint Creado / None
        """

        try:
            nombre = datos['nombre']
            descripcion = datos['descripcion']
            idProyecto = datos['idProyecto']
            fecha_inicio = datos['fechaInicio']
            fecha_fin = datos['fechaFin']
            capacidadEquipo = datos['capacidadEquipo']
            proyecto = Proyecto.objects.get(id=idProyecto)

            sprint = self.model(nombre=nombre, descripcion=descripcion,
                                proyecto=proyecto,
                                fecha_inicio=fecha_inicio,
                                fecha_fin=fecha_fin,
                                capacidadEquipo=capacidadEquipo)
            sprint.save()

            sprint = Sprint.objects.filter(id=sprint.id)
            return sprint
        except Exception as e:
            print("Error inesperado! " + str(e))
            return None

    def actualizarSprint(self, datos):
        pass

    def obtenerSprint(self, idProyecto, idSprint):
        """Retorna el Sprint, del proyecto con idProyecto, con el idSprint

                :param idProyecto: ID del proyecto
                :param idSprint: ID del sprint del proyecto

                :return: QuerySet de Sprint/ None
                """
        try:
            sprint = Sprint.objects.get(id=idSprint)
        except Sprint.DoesNotExist as e:
            print("No existe el sprint con el id dado! " + str(e))
            return None

        try:
            proyecto = Proyecto.objects.get(id=idProyecto)
        except Proyecto.DoesNotExist as e:
            print("No existe el proyecto con el id dado! " + str(e))
            return None

        # verificando si existe como sprint del proyecto dado
        if str(sprint.proyecto.id) == str(idProyecto):
            sprint = Sprint.objects.filter(id=sprint.id)
            return sprint
        else:
            print("El Sprint no pertenece al proyecto dado...")
            return None

    def eliminarSprint(self, idProyecto, idSprint):
        try:
            try:
                sprint = Sprint.objects.get(id=idSprint)
            except Sprint.DoesNotExist as e:
                print("No existe el sprint con el ID dado! " + str(e))
                return False

            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto con el ID dado! " + str(e))

            # verificando si existe como historia de usuario del proyecto dado
            if str(sprint.proyecto.id) == str(idProyecto):
                sprint.delete()
                return True
            else:
                print("El sprint no pertenece al proyecto dado...")
                return False
        except Exception as e:
            print("Error inesperado! " + str(e))
            return False



    def listarSprints(self, idProyecto):
        """Obtiene la lista completa de sprints de un proyecto

                :param idProyecto: ID del proyecto

                :return: QuerySet / None
                """
        try:
            proyecto = Proyecto.objects.get(id=idProyecto)
        except Proyecto.DoesNotExist as e:
            print("No existe el proyecto con el ID dado! " + str(e))
            return None

        listaSprints = Sprint.objects.filter(proyecto=idProyecto)
        return listaSprints


class ManagerMiembroSprint(models.Manager):

    def agregarMiembro(self, datos):

        capacidad = datos['capacidad']
        sprint_id = datos['sprint_id']
        usuario_id = datos['usuario_id']

        miembro_equipo = self.model(sprint_id=sprint_id, usuario_id=usuario_id, capacidad=capacidad)
        miembro_equipo.save()

        return miembro_equipo

    def modificarMiembro(self, datos):
        capacidad = datos['capacidad']
        miembro_id = datos['miembro_equipo_id']

        miembro_equipo = Sprint_Miembro_Equipo.objects.get(id=miembro_id)
        miembro_equipo.capacidad = capacidad
        miembro_equipo.save()

        return miembro_equipo

    def eliminarMiembro(self, idSprint, idProyecto, id_miembro_equipo):
        try:
            try:
                sprint = Sprint.objects.get(id=idSprint)
            except Sprint.DoesNotExist as e:
                print("No existe el sprint con el ID dado! " + str(e))
                return False

            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto con el ID dado! " + str(e))

            # verificando si existe como historia de usuario del proyecto dado
            if str(sprint.proyecto.id) == str(idProyecto):
                try:
                    miembro = Sprint_Miembro_Equipo.objects.get(id=id_miembro_equipo)
                    miembro.delete()
                except Sprint_Miembro_Equipo.DoesNotExist as e:
                    print('No existe el miembro con el id dado:' + str(e))

                return True
            else:
                print("El sprint no pertenece al proyecto dado...")
                return False
        except Exception as e:
            print("Error inesperado! " + str(e))
            return False


class ManagerSprintBacklog(models.Manager):
    def crearSprintBacklog(self):
        pass



class Sprint(models.Model):
    """
    Representación del modelo de Sprint


    Attributes
    ----------
    :fecha_inicio: DateField
        la fecha y hora prevista para el inicio del Sprint.
    :fecha_fin: DateTime
        la fecha y hora prevista para el final del Sprint.
    :capacidadEquipo: Integer
        capacidad, en horas, de trabajo asumible por el equipo del Sprint.
    :estado: Str
        Creado, En Espera, En Ejecucion, Culminado, Cancelado
    """
    nombre = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=200, null=True)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=False)
    capacidadEquipo = models.IntegerField(null=False)
    estado = models.TextField(max_length=10)
    proyecto = models.ForeignKey(Proyecto, null=False, on_delete=models.CASCADE)

    objects = ManagerSprint()

    def __str__(self):
        return str([self.fecha_inicio, self.fecha_fin, self.capacidadEquipo,
                    self.estado])


class SprintBacklog(models.Model):
    """
          Representación del modelo de backlog de Sprint


        Attributes
        ----------
        :idHistoriaUsuario: Historia_Usuario
            Foreign key a una historia de usuario (la lista de historias
            es lo que forma el Backlog)
        :idSprint: Sprint
            Foreign key del Sprint al cual está asociado este Backlog
    """


    idHistoriaUsuario = models.ManyToManyField(historiaUsuario)
    idSprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=False)

    objects = ManagerSprintBacklog()

    def __str__(self):
        return str([self.idSprint.id])

class Sprint_Miembro_Equipo(models.Model):
    """
        Miembro del equipo de un Sprint dado

        Attributes
        ----------
        :usuario: Usuario
            Foreign Key al usuario participante de este equipo
        :sprint: Sprint
            Foreign Key referenciando el Sprint al cual este usuario
            pertenece.
        :capacidad: IntegerField
            Capacidad (int en horas) del Usuario participante de este equipo
    """

    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    capacidad = models.IntegerField()

    objects = ManagerMiembroSprint()

    def __str__(self):
        return str([self.usuario.id, self.sprint.id,
                    self.capacidad.__str__()])

