import datetime

from django.db import models

from proyectos.models import Proyecto
from usuarios.models import Usuario
from historiasDeUsuario_proyecto.models import historiaUsuario

class ManagerSprint(models.Manager):

    def crearSprint(self, datos):
        """Crea una historia de usuario

        :param datos: Diccionario (o JSON) con los siguientes valores "key":
        nombre, descripcion, idProyecto, fechaInicio, fechaFin, capacidadEquipo.

        :return: QuerySet de Sprint Creado / None
        """

        try:
            nombre = datos['nombre']
            descripcion = datos['descripcion']
            idProyecto = datos['idProyecto']
            capacidadEquipo = datos['capacidadEquipo']
            cantidadDias = datos['cantidadDias']
            proyecto = Proyecto.objects.get(id=idProyecto)

            sprint = self.model(nombre=nombre, descripcion=descripcion,
                                proyecto=proyecto,
                                fecha_inicio=None,
                                fecha_fin=None,
                                cantidadDias=cantidadDias,
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

    def cambiarEstado(self, idProyecto, idSprint, opcion):
        """Cambia el estado de un sprint

        :param idProyecto: ID del proyecto al que pertenece el sprint
        :param idSprint: ID del sprint
        :param opcion: Str, Avanzar/Cancelar
        Avanzar cambia el estado: Planificacion -> En Ejecucion -> Finalizado

        :return: QuerySet del Sprint actualizado/None
        """

        try:

            try:
                sprint = Sprint.objects.get(id=idSprint)
            except Sprint.DoesNotExist as e:
                print("No existe el sprint! " + str(e))
                return None

            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto! " + str(e))
                return None
            if sprint.proyecto_id == proyecto.id:
                if opcion == 'Avanzar':
                    if sprint.estado == "Planificación":
                        sprint.estado = "En Ejecución"

                        # Agregamos la cantidad de dias de duracion que va a tener el proyecto
                        fechahoy = datetime.date.today()
                        sprint.fecha_inicio = fechahoy
                        sprint.fecha_fin = fechahoy + datetime.timedelta(days=sprint.cantidadDias)
                        SprintBacklog.objects.crearSprintBacklog(proyecto_id=idProyecto, sprint_id=idSprint)
                    elif sprint.estado == "En Ejecución":
                        sprint.estado = "Finalizado"

                    sprint.save()
                    return Sprint.objects.filter(id=sprint.id)
                elif opcion == 'Cancelar':
                    sprint.estado = "Cancelado"
                    sprint.save()
                    return Sprint.objects.filter(id=sprint.id)
                else:
                    print("Opcion invalida! ")
                    return None
            else:
                print("El sprint no pertenece al proyecto dado! ")
                return None
        except Exception as e:
            print("No se pudo actualizar el estado del sprint! " + str(e))
            return None



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
    def crearSprintBacklog(self, proyecto_id, sprint_id):

        # Lista de HU ordenada por prioridad
        #lista_hu_ordenada = historiaUsuario.objects.filter(proyecto_id = proyecto_id).order_by('prioridad_tecnica').reverse()

        self.actualizarPrioridadFinal(self, proyecto_id)
        lista_hu_ordenada = historiaUsuario.objects.filter(proyecto_id=proyecto_id).order_by('prioridad_final').reverse()

        sprint = Sprint.objects.get(id=sprint_id)
        capacidad_sprint = sprint.capacidadEquipo

        # Crear Sprint Backlog
        sprint_backlog = SprintBacklog.objects.model(idSprint_id=sprint_id)
        sprint_backlog.save()

        # Añadir HU según la capacidad del Sprint
        acumulado = 0

        for historia_usuario in lista_hu_ordenada:
            if acumulado >= capacidad_sprint: # Si llenamos la capacidad del Sprint, terminamos de añadir HU
                break

            if not (historia_usuario.estado=="cancelada" or historia_usuario.estado=="finalizada"):
                sprint_backlog.historiaUsuario.add(historia_usuario)
                horas_hu = historia_usuario.estimacion_horas
                acumulado += horas_hu

    def actualizarPrioridadFinal(self, proyecto_id):
        lista_hu_ordenada = historiaUsuario.objects.filter(proyecto_id=proyecto_id).order_by(
            'prioridad_tecnica').reverse()

        for hu in lista_hu_ordenada:
            hu.prioridad_final = round(0.6*hu.prioridad_negocio + 0.4*hu.prioridad_tecnica) # Redondea el valor decimal
            if hu.horas_trabajadas is not None:
                if hu.horas_trabajadas > 0:
                    hu.prioridad_final += 3
            hu.save()

    def listarHistoriasUsuario(self, proyecto_id, sprint_id):
        """Retorna la lista de historias de usuario asociadas al sprint del proyecto dado

        :param proyecto_id: ID del proyecto
        :param sprint_id: ID del sprint

        :return: QuerySet de lista de US/None
        """
        try:
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
            except Proyecto.DoesNotExist as e:
                print("El proyecto no existe!")
                return None

            try:
                sprint = Sprint.objects.get(id=sprint_id)
            except Sprint.DoesNotExist as e:
                print("El sprint no existe!")
                return None

            # Verificando que el sprint pertenezca al proyecto dado
            if sprint.proyecto_id == proyecto.id:
                try:
                    backlog = SprintBacklog.objects.get(idSprint=sprint.id)
                except SprintBacklog.DoesNotExist as e:
                    print("No existe el sprintbacklog! " + str(e))
                    return None

                return backlog.historiaUsuario.all()
        except Exception as e:
            print("Error al obtener la lista de US! " + str(e))
            return None

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
        Planificación, Ejecución, Finalizado, Cancelado
    """
    nombre = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=200, null=True)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    cantidadDias = models.IntegerField(null=True)
    capacidadEquipo = models.IntegerField(null=False)
    estado = models.TextField(max_length=20, default='Planificación')
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


    historiaUsuario = models.ManyToManyField(historiaUsuario)
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

