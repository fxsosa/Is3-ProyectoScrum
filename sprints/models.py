import datetime
from django.utils import timezone
from django.db import models
import pytz

from historiasDeUsuario.models import Tipo_Historia_Usuario, Columna_Tipo_Historia_Usuario
from proyectos.models import Proyecto
from usuarios.models import Usuario
from historiasDeUsuario_proyecto.models import historiaUsuario

import numpy as np

class ManagerSprint(models.Manager):

    def crearSprint(self, datos):
        """Crea un sprint de proyecto

        :param datos: Diccionario (o JSON) con los siguientes valores "key":
        nombre, descripcion, idProyecto, cantidadDias, capacidadEquipo.

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
            # creamos el sprint backlog
            SprintBacklog.objects.crearSprintBacklog(sprint.id)

            sprint = Sprint.objects.filter(id=sprint.id)
            return sprint
        except Exception as e:
            print("Error inesperado! " + str(e))
            return None

    def actualizarSprint(self, datos):
        """Actualizar los parametros de un Sprint

        :param datos: Diccionario JSON con los siguientes parametros: "idProyecto", "idSprint" "nombre", "descripcion", "cantidadDias"

        :return: QuerySet de Sprint actualizado/None
        """

        try:
            try:
                proyecto = Proyecto.objects.get(id=datos['idProyecto'])
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto!")
                return None

            try:
                sprint = Sprint.objects.get(id=datos["idSprint"])
            except Sprint.DoesNotExist as e:
                print("No existe el sprint!")
                return None

            # verificando si existe como sprint del proyecto dado
            if str(sprint.proyecto.id) == str(proyecto.id):
                if datos["nombre"] is not None:
                    sprint.nombre = datos["nombre"]

                if datos["descripcion"] is not None:
                    sprint.descripcion = datos["descripcion"]

                if datos["cantidadDias"] is not None:
                    sprint.cantidadDias = datos["cantidadDias"]

                sprint.save()

                return Sprint.objects.filter(id=sprint.id)
            else:
                print("El sprint no pertenece al proyecto dado! ")
                return None
        except Exception as e:
            print("No se pudo actualizar sprint! " + str(e))
            return None


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
        """Eliminar un sprint de un proyecto

        :param idProyecto: ID del proyecto
        :param idSprint: ID de un sprint

        :return: Boolean
        """

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
                # sprint.delete()
                # Cambiamos el estado del sprint a Cancelado
                sprint.estado = "Cancelado"
                sprint.save()
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

        :return: QuerySet del Sprint actualizado/String
        """

        try:

            try:
                sprint = Sprint.objects.get(id=idSprint)
            except Sprint.DoesNotExist as e:
                print("No existe el sprint! " + str(e))
                return "No existe el sprint!"

            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto! " + str(e))
                return "No existe el proyecto!"

            if sprint.proyecto_id == proyecto.id:
                if opcion == 'Avanzar':

                    if sprint.estado == "Creado": # Este sería un Sprint creado que no está en planificación
                        if Sprint.objects.filter(proyecto=proyecto.id, estado="Planificación").exists():
                            print("Ya existe un sprint en planificación en este proyecto! ")
                            return "Operación no permitida.\nYa existe un sprint \"En Planificación\" en este proyecto! "
                        else:
                            sprint.estado = "Planificación"
                            sprint.save()

                    elif sprint.estado == "Planificación":

                        # Query de todos los sprints del proyecto que tengan estado=En Ejecución
                        if Sprint.objects.filter(proyecto=proyecto.id, estado="En Ejecución").exists():
                            print("Ya existe un sprint en ejecucion en este proyecto! ")
                            return "Operación no permitida.\nYa existe un sprint \"En Ejecución\" en este proyecto! "
                        else:

                            # Verificando que el sprint solo puede estar En Ejecucion cuando el proyecto se encuentra
                            # en estado 'iniciado'
                            if proyecto.estado != "iniciado":
                                print("Operacion no permitida.\nEl sprint no puede iniciarse hasta que el proyecto sea iniciado!")
                                return "Operacion no permitida.\nEl sprint no puede iniciarse hasta que el proyecto sea iniciado!"

                            # Verificando que el sprint tenga al menos un desarrollador asignado para poder iniciar
                            if Sprint_Miembro_Equipo.objects.filter(sprint_id=sprint.id).count() == 0:
                                print("Operacion no permitida.\nEl sprint no puede iniciarse sin participantes!")
                                return "Operacion no permitida.\nEl sprint no puede iniciarse sin participantes!"


                            sprint.estado = "En Ejecución"

                            # Agregamos la cantidad de dias de duracion que va a tener el proyecto
                            # fechahoy = datetime.date.today()
                            fechahoy = timezone.now()
                            sprint.fecha_inicio = fechahoy
                            sprint.fecha_fin = self.calcularFechaFinal( fecha_inicio=fechahoy, cantidadDias=sprint.cantidadDias)
                            sprint.save()
                    elif sprint.estado == "En Ejecución":
                        fechahoy = timezone.now()
                        sprint.fecha_fin = fechahoy
                        sprint.estado = "Finalizado"
                        sprint.save()

                    return Sprint.objects.filter(id=sprint.id)

                elif opcion == 'Cancelar':
                    sprint.estado = "Cancelado"
                    sprint.save()
                    return Sprint.objects.filter(id=sprint.id)
                else:
                    print("Opcion invalida! ")
                    return "No se pudo actualizar el estado del sprint!"
            else:
                print("El sprint no pertenece al proyecto dado! ")
                return "No se pudo actualizar el estado del sprint! "
        except Exception as e:
            print("No se pudo actualizar el estado del sprint! " + str(e))
            return "No se pudo actualizar el estado del sprint! "


    def calcularFechaFinal(self, fecha_inicio, cantidadDias):
        """
        Retorna la fecha final luego de que pasen una cierta cantidad de días laborales (cantidadDias)
        Parameters
        ----------
        fecha_inicio: date
        cantidadDias: integer

        Returns date
        -------

        """

        dias_acumulados = 0
        fecha_fin = fecha_inicio + datetime.timedelta(days=cantidadDias)
        dias_laborales = np.busday_count(fecha_inicio.date(), fecha_fin.date())


        while dias_laborales < cantidadDias-1: # Por alguna razón el -1 hace que sí de el resultado correcto xd
            dias_acumulados += 1
            dias_totales = cantidadDias + dias_acumulados
            fecha_fin = fecha_inicio + datetime.timedelta(days=dias_totales)
            dias_laborales = np.busday_count(fecha_inicio.date(), fecha_fin.date())

        return fecha_fin

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
        """Agrega a un usuario como miembro de un sprint.

        :param datos: Diccionario. Tiene los siguientes parametros: "capacidad" (Entero), "sprint_id", "usuario_id"

        :return: Objeto Miembro Sprint
        """

        capacidad = datos['capacidad']
        sprint_id = datos['sprint_id']
        usuario_id = datos['usuario_id']

        miembro_equipo = Sprint_Miembro_Equipo(sprint_id=sprint_id, usuario_id=usuario_id, capacidad=capacidad)
        miembro_equipo.save()

        ManagerSprintBacklog.calcularCapacidadSprint(ManagerSprintBacklog, sprint_id)


        return miembro_equipo

    def modificarMiembro(self, datos):
        """Modifica los datos de un usuario asignado como miembro de sprint

        :param datos: Diccionario. Tiene los siguientes parametros:
        "capacidad": Capacidad en horas que un usuario puede trabajar al dia
        "miembro_id": ID del miembro del sprint

        :return:
        """

        capacidad = datos['capacidad']
        miembro_id = datos['miembro_equipo_id']
        sprint_id = datos['sprint_id']

        miembro_equipo = Sprint_Miembro_Equipo.objects.get(id=miembro_id)
        miembro_equipo.capacidad = capacidad
        miembro_equipo.save()

        ManagerSprintBacklog.calcularCapacidadSprint(ManagerSprintBacklog, sprint_id)

        return miembro_equipo

    def eliminarMiembro(self, idSprint, idProyecto, id_miembro_equipo):
        """Elimina un miembro de un sprint

        :param idSprint: ID del sprint
        :param idProyecto: ID del proyecto
        :param id_miembro_equipo: ID del miembro de un equipo

        :return: Boolean
        """

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
                    ManagerSprintBacklog.calcularCapacidadSprint(ManagerSprintBacklog, idSprint)
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

    def crearSprintBacklog(self, sprint_id):
        sprint_backlog = SprintBacklog.objects.model(idSprint_id=sprint_id)
        sprint_backlog.save()

    def crearSprintBacklogViejo(self, proyecto_id, sprint_id):
        """Crea un sprint backlog. Agrega las US permitidas del proyecto.

        :param proyecto_id: ID del proyecto
        :param sprint_id: ID del sprint

        """
        # Lista de HU ordenada por prioridad
        #lista_hu_ordenada = historiaUsuario.objects.filter(proyecto_id = proyecto_id).order_by('prioridad_tecnica').reverse()

        self.calcularCapacidadSprint(self, sprint_id)
        self.actualizarPrioridadFinal(self, proyecto_id)
        lista_hu_ordenada = historiaUsuario.objects.filter(proyecto_id=proyecto_id).order_by('prioridad_final').reverse()

        sprint = Sprint.objects.get(id=sprint_id)
        capacidad_sprint = sprint.capacidadEquipo

        print("Capacidad del equipo es: ")
        print(sprint.capacidadEquipo)

        # Crear Sprint Backlog
        sprint_backlog = SprintBacklog.objects.model(idSprint_id=sprint_id)
        sprint_backlog.save()

        # Añadir HU según la capacidad del Sprint
        acumulado = 0

        for historia_usuario in lista_hu_ordenada:
            if acumulado >= capacidad_sprint: # Si llenamos la capacidad del Sprint, terminamos de añadir HU
                break

            # Verificamos:
            # 1. Estado de la US no sea cancelada ni finalizada
            # 2. Tiene desarrollador asignado encargado de la US
            # 3. El desarrollador asignado es miembro del equipo del sprint al cual se agrega la US
            if not (historia_usuario.estado=="cancelada" or historia_usuario.estado=="finalizada" or historia_usuario.desarrollador_asignado is None):
                # Verificamos el Nro. 3
                if Sprint_Miembro_Equipo.objects.filter(usuario_id=historia_usuario.desarrollador_asignado.usuario.id, sprint_id=sprint.id).exists():
                    columnas = Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=historia_usuario.tipo_historia_usuario_id).order_by('orden')
                    historia_usuario.estado = columnas[0].id
                    print('historia_usuario.estado', historia_usuario.estado)
                    historia_usuario.save()

                    sprint_backlog.historiaUsuario.add(historia_usuario)
                    horas_hu = historia_usuario.estimacion_horas
                    acumulado += horas_hu

    def actualizarPrioridadFinal(self, proyecto_id):
        """Actualiza las prioridades de los US de un proyecto.

        :param proyecto_id:
        :return: None
        """

        lista_hu_ordenada = historiaUsuario.objects.filter(proyecto_id=proyecto_id).order_by(
            'prioridad_tecnica').reverse()

        for hu in lista_hu_ordenada:
            hu.prioridad_final = round(0.6*hu.prioridad_negocio + 0.4*hu.prioridad_tecnica) # Redondea el valor decimal
            if hu.horas_trabajadas is not None:
                if hu.horas_trabajadas > 0:
                    hu.prioridad_final += 3
            hu.save()

    def calcularCapacidadSprint(self, sprint_id):
        """
        Calculamos la capacidad total del Sprint
        :param sprint_id: ID del sprint

        """
        listaEquipo = Sprint_Miembro_Equipo.objects.filter(sprint_id=sprint_id)
        capacidad_horas_diarias = 0
        # Calculamos total de horas por día que se le dedica al sprint
        for miembro in listaEquipo:
            capacidad_horas_diarias += miembro.capacidad

        sprint = Sprint.objects.get(id=sprint_id)

        dias_laborales = sprint.cantidadDias

        capacidad_total = capacidad_horas_diarias*dias_laborales

        sprint.capacidadEquipo = capacidad_total
        sprint.save()

    def listarTipoHUSprint(self, idProyecto, idSprint):
        """Listar los tipos de HU que pertenecen a un proyecto y se usan en un sprint

        :param idProyecto: ID del proyecto
        :param idSprint: ID del sprint de proyecto

        :return: QuerySet de Tipos de US/None
        """

        try:
            listaUS = self.listarHistoriasUsuario(proyecto_id=idProyecto, sprint_id=idSprint)
            # Guardamos en un set (no permite duplicados) la lista de IDs de los tipos de US
            setUSTipo = set()
            for historia in listaUS:
                setUSTipo.add(historia.tipo_historia_usuario.id)

            if len(setUSTipo) == 0:
                print("No hay US asociada a este Sprint")
                return None

            listatipos = Tipo_Historia_Usuario.objects.filter(id__in=list(setUSTipo))

            return listatipos

        except Exception as e:
            print("Error al obtener la lista de Tipos de US! " + str(e))
            return None

    def listarHistoriasUsuario(self, proyecto_id, sprint_id):
        """Retorna la lista de historias de usuario asociadas al sprint del proyecto dado

        :param proyecto_id: ID del proyecto
        :param sprint_id: ID del sprint

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

                return backlog.historiaUsuario.all().order_by('-prioridad_final')
        except Exception as e:
            print("Error al obtener la lista de US! " + str(e))
            return None


    def listarHUTipo(self, proyecto_id, sprint_id, tipo_id):
        """Retorna la lista de historias de usuario de un tipo, asociadas al sprint del proyecto dado

        :param proyecto_id: ID del proyecto
        :param sprint_id: ID del sprint
        :param tipo_id: ID del tipo de US

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

            try:
                tipoHU = Tipo_Historia_Usuario.objects.get(id=tipo_id)
            except Tipo_Historia_Usuario.DoesNotExist as e:
                print("El tipo de US no existe!")
                return None

            # Verificando que el sprint pertenezca al proyecto dado
            # y que el tipo pertenezca al proyecto
            if sprint.proyecto_id == proyecto.id and tipoHU.proyecto.filter(id=proyecto_id).exists():
                try:
                    backlog = SprintBacklog.objects.get(idSprint=sprint.id)
                except SprintBacklog.DoesNotExist as e:
                    print("No existe el sprintbacklog! " + str(e))
                    return None

                # Retornando la lista de US con el tipo de HU especificado
                return backlog.historiaUsuario.filter(proyecto_id=proyecto_id, tipo_historia_usuario_id=tipo_id)
        except Exception as e:
            print("Error al obtener la lista de US del tipo especificado! " + str(e))
            return None

    def agregarHUSprintBacklog(self, idProyecto, idSprint, idHistoria):
        """Agrega una historia de usuario al sprint backlog

            :param idProyecto: ID del proyecto
            :param idSprint: ID del sprint
            :param idHistoria: ID de la historia de usuario a eliminar

            :return: Boolean
            """
        try:
            try:
                sprint = Sprint.objects.get(id=idSprint)
            except Sprint.DoesNotExist as e:
                print("No existe el sprint con el ID dado! " + str(e))
                return False

            try:
                sprintbacklog = SprintBacklog.objects.get(idSprint=idSprint)
            except SprintBacklog.DoesNotExist as e:
                print("No existe el sprintbacklog! " + str(e))
                return False

            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto con el ID dado! " + str(e))
                return False

            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print("No existe la historia de usuario con el ID dado! " + str(e))
                return False

            # verificando si existe como sprint del proyecto dado
            # y verificando que la historia de usuario este asociada al sprintbacklog
            if str(sprint.proyecto.id) == str(idProyecto):
                # Removemos la historia de usuario del sprint backlog
                sprintbacklog.historiaUsuario.add(historia)
                return True
            else:
                print("El sprint no pertenece al proyecto")
                return False
        except Exception as e:
            print("Error inesperado: " + str(e))
            return False



    def eliminarHUSprintBacklog(self, idProyecto, idSprint, idHistoria):
        """Eliminar la historia de usuario del sprint backlog

        :param idProyecto: ID del proyecto
        :param idSprint: ID del sprint
        :param idHistoria: ID de la historia de usuario a eliminar

        :return: Boolean
        """
        try:
            try:
                sprint = Sprint.objects.get(id=idSprint)
            except Sprint.DoesNotExist as e:
                print("No existe el sprint con el ID dado! " + str(e))
                return False

            try:
                sprintbacklog = SprintBacklog.objects.get(idSprint=idSprint)
            except SprintBacklog.DoesNotExist as e:
                print("No existe el sprintbacklog! " + str(e))
                return False

            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("No existe el proyecto con el ID dado! " + str(e))
                return False

            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print("No existe la historia de usuario con el ID dado! " + str(e))
                return False

            # verificando si existe como sprint del proyecto dado
            # y verificando que la historia de usuario este asociada al sprintbacklog
            if str(sprint.proyecto.id) == str(idProyecto) \
                    and sprintbacklog.historiaUsuario.filter(id=idHistoria).exists():
                # Removemos la historia de usuario del sprint backlog
                sprintbacklog.historiaUsuario.remove(historia)
                sprintbacklog.save()
                return True
            else:
                print("El sprint no pertenece al proyecto o la historia no pertenece al sprint...")
                return False
        except Exception as e:
            print("Error inesperado! " + str(e))
            return False



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
    estado = models.TextField(max_length=20, default='Creado')
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
    capacidad = models.IntegerField() # Horas diarias que puede dedicar

    objects = ManagerMiembroSprint()

    def __str__(self):
        return str([self.usuario.id, self.sprint.id,
                    self.capacidad.__str__()])

