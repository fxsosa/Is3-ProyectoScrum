from django.conf import settings
from django.db import models
from django.db.migrations import serializer
from simple_history.management.commands.populate_history import get_model
from simple_history.models import HistoricalRecords
import json
import proyectos
import sprints
import usuarios.models
from django.core import serializers
from historiasDeUsuario.models import Tipo_Historia_Usuario, Columna_Tipo_Historia_Usuario
from proyectos.models import participante, Proyecto
from usuarios.models import Usuario
from itertools import chain
import smtplib
import ssl
from email.message import EmailMessage



class managerHistoriaUsuario(models.Manager):
    def crearHistoriaUsuario(self, datos, user):
        """Crea una historia de usuario

        :param datos: Diccionario (o JSON) con los siguientes valores "key":
        - nombre: Nombre de la historia de usuario a crear,
        - descripcion: Descripcion de la historia de usuario,
        - prioridad_tecnica: Prioridad (entero),
        - prioridad_negocio: Prioridad (entero),
        - estimacion_horas: Estimacion en horas (entero),
        - idTipo: ID del registro del modelo Tipo_Historia_Usuario,
        - idParticipante: ID del participante del proyecto,
        - idProyecto: ID del proyecto al cual pertenecera esta historia de usuario
        user: Instancia de Custom Usuario que realiza el cambio

        :return: QuerySet de Historia de Usuario Creada / None
        """

        try:
            nombre = datos['nombre']
            descripcion = datos['descripcion']
            prioridad_tecnica = int(datos['prioridad_tecnica'])
            prioridad_negocio = int(datos['prioridad_negocio'])

            # Agregamos prioridad_general en caso de que ya tengamos la prioridad tecnica y de negocio
            prioridad_final = None
            if prioridad_tecnica is not None and prioridad_negocio is not None:
                # Verificamos que este dentro de [0;10], sino, dejamos en cero
                if prioridad_tecnica < 0 or prioridad_tecnica > 10:
                    prioridad_tecnica = 0

                # Verificamos que este dentro de [0;10], sino, dejamos en cero
                if prioridad_negocio < 0 or prioridad_negocio > 10:
                    prioridad_negocio = 0

                prioridad_final = round(0.6 * prioridad_negocio + 0.4 * prioridad_tecnica) # Redondea el valor decimal

            estimacion_horas = datos['estimacion_horas']
            idTipo = datos['idTipo']
            if datos['idTipo']:
                tipoHistoria = Tipo_Historia_Usuario.objects.get(id=idTipo)
            else:
                tipoHistoria = None

            proyecto = Proyecto.objects.get(id=datos['idProyecto'])

            idParticipante = datos['idParticipante'] # Participante asignado
            if datos['idParticipante']:
                # Verificamos el desarrollador pertenezca al proyecto recibido
                try:
                    desarrollador = participante.objects.get(id=idParticipante, proyecto_id=proyecto.id)
                except participante.DoesNotExist as e:
                    print(e)
                    desarrollador = None
            else:
                desarrollador = None


            historia = self.model(nombre=nombre, descripcion=descripcion,
                                  prioridad_tecnica=prioridad_tecnica,
                                  prioridad_negocio=prioridad_negocio,
                                  estimacion_horas=estimacion_horas,
                                  prioridad_final=prioridad_final,
                                  tipo_historia_usuario=tipoHistoria,
                                  desarrollador_asignado=None,
                                  proyecto=proyecto)
            historia.changed_by = user
            historia.save()
            cambiarMotivoHistorial(historia, "Creado")
            historia = historiaUsuario.objects.filter(id=historia.id)
            return historia
        except Exception as e:
            print(e)
            return None

    def eliminarHistoriaUsuario(self, idProyecto, idHistoria, user):
        """Elimina de forma lógica una Historia de Usuario

        :param datos:
        - idHistoria: ID de la Historia de Usuario,
        - idProyecto: ID del proyecto al cual pertenecera esta historia de usuario
        - user: Instancia de Custom Usuario que realiza el cambio

        :return: boolean
        """

        try:
            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print(e)
                return False

            # verificando si existe como historia de usuario del proyecto dado
            if str(historia.proyecto.id) == str(idProyecto): # Procede a realizar la eliminación lógica
                #historia.delete()
                historia.estado = "cancelada"
                historia.changed_by = user
                historia.save()
                cambiarMotivoHistorial(historia, "Cancelado")
                return True
            else:
                print("La historia de usuario no pertenece al proyecto dado...")
                return False
        except Exception as e:
            print(e)
            return False

    def actualizarHistoriaUsuario(self, datos, esDev, user):
        try:
            idProyecto = datos['idProyecto']
            idHistoria = datos['idHistoria']
            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print(e)
                return None

            modificado = False

            # actualizaciones solo para scrum masters
            if not esDev:
                if datos['idParticipante'] is not None:
                    try:
                        print(datos['idParticipante'])
                        usuarioParticipante = Usuario.objects.get(id=datos['idParticipante'])
                        desarrollador = participante.objects.get(proyecto_id=idProyecto, usuario_id=usuarioParticipante)

                    except participante.DoesNotExist as e:
                        print("Participante no existe! + " + str(e))
                        return None

                if datos['idTipo'] is not None:
                    try:
                        tipoHistoria = Tipo_Historia_Usuario.objects.get(id=datos['idTipo'])
                    except Tipo_Historia_Usuario.DoesNotExist as e:
                        print("Tipo de historia de usuario no existe! + " + str(e))
                        return None

                # verificando si existe como historia de usuario del proyecto dado
                if str(historia.proyecto.id) == str(idProyecto):
                    if datos['nombre'] is not None:
                        historia.nombre = datos['nombre']
                        modificado = True

                    if datos['descripcion'] is not None:
                        historia.descripcion = datos['descripcion']
                        modificado = True

                    if datos['prioridad_tecnica'] is not None and datos['prioridad_tecnica'] >= 0 and datos['prioridad_tecnica'] <= 10:
                        historia.prioridad_tecnica = datos['prioridad_tecnica']
                        modificado = True

                    if datos['prioridad_negocio'] is not None and datos['prioridad_negocio'] >= 0 and datos['prioridad_negocio'] <=10:
                        historia.prioridad_negocio = datos['prioridad_negocio']
                        modificado = True

                    # Actualizamos la prioridad final en caso de que se haya actualizado alguna prioridad
                    if datos['prioridad_negocio'] is not None or datos['prioridad_tecnica'] is not None:
                        if historia.prioridad_negocio is not None and historia.prioridad_tecnica is not None:
                            historia.prioridad_final = round(0.6 * historia.prioridad_negocio + 0.4 * historia.prioridad_tecnica)  # Redondea el valor decimal
                            if historia.sprints_trabajados is not None:
                                historia.prioridad_final += 3 * historia.sprints_trabajados

                    if datos['estimacion_horas'] is not None:
                        historia.estimacion_horas = datos['estimacion_horas']
                        modificado = True

                    if datos['idTipo'] is not None:
                        historia.tipo_historia_usuario = tipoHistoria
                        modificado = True

                    if datos['idParticipante'] is not None:
                        historia.desarrollador_asignado = desarrollador
                        modificado = True

                else:
                    print("La historia de usuario no pertenece al proyecto dado...")
                    return None

            # actualizaciones para devs
            if datos['horas_trabajadas'] is not None:
                historia.horas_trabajadas = datos['horas_trabajadas']
                modificado = True


            if datos['estado'] is not None:
                # obtenemos el tipo y su columna
                columnaId = datos['estado']
                if columnaId == 'rechazada' or columnaId == 'aceptada':
                    if esDev:
                        print('No es Scrum Master, no se puede cambiar estado')
                    else:
                        historia.estado = datos['estado']
                        modificado = True

                elif columnaId != 'cancelada':
                    try:
                        columna = Columna_Tipo_Historia_Usuario.objects.get(id=columnaId)

                        columnaOrden = columna.orden
                        cantidadCol = len(Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=historia.tipo_historia_usuario_id))

                        # verificar si se paso a la ultima columna
                        if columnaOrden == cantidadCol:
                            datos['estado'] = 'finalizada'

                            # Notificar a Scrum Master
                            proyecto = Proyecto.objects.get(id=idProyecto)
                            nombreProyecto = proyecto.nombre

                            idScrumMaster = proyecto.scrumMaster_id
                            scrumMaster = Usuario.objects.get(id=idScrumMaster)

                            mail = scrumMaster.email
                            titulo = "Nueva Historia de Usuario pendiente de revisión"
                            cuerpo = "El proyecto " + nombreProyecto + " tiene una nueva Historia de Usuario pendiente de revisión"

                            managerHistoriaUsuario.mandarEmail(managerHistoriaUsuario, mail, titulo, cuerpo)


                            modificado = True

                        if historia.estado != datos['estado']:
                            historia.estado = datos['estado']
                            modificado = True

                    except Columna_Tipo_Historia_Usuario.DoesNotExist as e:
                        historia.estado = None
                        print("No existe la columna!")
                else:
                    historia.estado = 'cancelada'

            if modificado is True:
                historia.changed_by = user
                historia.save()
                cambiarMotivoHistorial(historia, "Actualizado")

            historia = historiaUsuario.objects.filter(id=historia.id)
            return historia


        except Exception as e:
            print("error en: ",e)
            return None

    def mandarEmail(self, email_destinatario, asunto, cuerpo):
        """

        Parameters
        ----------
        email_recibe: Cadena con el email del destinatario
        asunto: Asunto del mail
        cuerpo: Contenido del mail

        Returns
        -------

        """
        # Define email sender and receiver
        email_sender = 'proyectoscrum5@gmail.com'
        email_password = 'ingenieriadesoftware2'
        email_receiver = email_destinatario

        # Set the subject and body of the email
        subject = asunto
        body = cuerpo

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


    def obtenerHistoriaUsuario(self, idProyecto, idHistoria):
        """Retorna la historia de usuario del proyecto dado con el id idHistoria

        :param idProyecto: ID del proyecto
        :param idHistoria: ID de la Historia de Usuario del proyecto

        :return: QuerySet / None
        """
        try:
            historia = historiaUsuario.objects.get(id=idHistoria)
        except historiaUsuario.DoesNotExist as e:
            print(e)
            return None

        # verificando si existe como historia de usuario del proyecto dado
        if str(historia.proyecto.id) == str(idProyecto):
            historia = historiaUsuario.objects.filter(id=historia.id)
            return historia
        else:
            print("La historia de usuario no pertenece al proyecto dado...")
            return None

    def listarHistoriasUsuario(self, idProyecto):
        """Obtiene la lista completa de historias de usuario. Obtiene la lista completa de historias de usuario. Se ordenan de acuerdo a la prioridad de las US.
        Las historias canceladas se muestran al final de la lista

        :param idProyecto: ID del proyecto

        :return: QuerySet / None
        """
        try:
            proyecto = Proyecto.objects.get(id=idProyecto)
        except Proyecto.DoesNotExist as e:
            print(e)
            return None

        # Extraemos las historias canceladas (para poner al final de la lista retorno)
        listaHistoriasCanceladas = historiaUsuario.objects.filter(proyecto=idProyecto, estado="cancelada").order_by("-prioridad_final")

        # Lista de historias finalizadas (para poner en el medio de la lista)
        listaHistoriasFinalizadas = historiaUsuario.objects.filter(proyecto=idProyecto, estado="finalizada").order_by("-prioridad_final")

        # Lista de historias aceptadas (cuyo release fue aceptado por el Scrum Master
        listaHistoriasAceptadas = historiaUsuario.objects.filter(proyecto=idProyecto, estado="aceptada").order_by(
            "-prioridad_final")

        # Lista de historias no finalizadas ni canceladas ni aceptadas (estas historias incluyen las rechazadas por el Scrum Master)
        listaHistoriasRestantes = historiaUsuario.objects.filter(proyecto=idProyecto).exclude(estado__in=["cancelada", "finalizada", "aceptada"]).order_by("-prioridad_final")

        listaHistorias = list(chain(listaHistoriasRestantes, listaHistoriasFinalizadas, listaHistoriasAceptadas, listaHistoriasCanceladas))

        return listaHistorias


    def listarHistoriasFinalizadas(self, idProyecto):
        """
        Método para obtener las Historia de Usuario Finalizadas
        Tiene utilidad para el Scrum Master, que podrá revisar las historias finalizadas
        para aprobar o rechazar su release

        Parameters
        ----------
        idProyecto: ID del Proyecto

        Returns listaHistorias: Lista de Historias Finalizadas
        -------

        """
        try:
            proyecto = Proyecto.objects.get(id=idProyecto)
        except Proyecto.DoesNotExist as e:
            print(e)
            return None

        # Lista de historias finalizadas (para poner en el medio de la lista)
        listaHistoriasFinalizadas = historiaUsuario.objects.filter(proyecto=idProyecto, estado="finalizada").order_by(
            "-prioridad_final")


        listaHistorias = list(listaHistoriasFinalizadas)

        return listaHistorias

    def listarHUTipo(self, idProyecto, idTipoHU):
        """Retorna la lista de historias de usuario de un tipo, asociadas al sprint del proyecto dado

                :param proyecto_id: ID del proyecto
                :param sprint_id: ID del sprint
                :param tipo_id: ID del tipo de US

                :return: QuerySet de lista de US/None
                """
        try:
            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("El proyecto no existe!")
                return None

            try:
                tipoHU = Tipo_Historia_Usuario.objects.get(id=idTipoHU)
            except Tipo_Historia_Usuario.DoesNotExist as e:
                print("El tipo de US no existe!")
                return None

            # Verificando que el sprint pertenezca al proyecto dado
            # y que el tipo pertenezca al proyecto
            if tipoHU.proyecto.filter(id=idProyecto).exists():

                # Retornando la lista de US con el tipo de HU especificado
                return historiaUsuario.objects.filter(proyecto_id=idProyecto, tipo_historia_usuario_id=idTipoHU)
        except Exception as e:
            print("Error al obtener la lista de US del tipo especificado! " + str(e))
            return None

    def listarHistorialUS(self, idProyecto, idHistoria):
        """Retorna el historial de cambios de una historia de usuario, de un proyecto con el id idHistoria

                :param idProyecto: ID del proyecto
                :param idHistoria: ID de la Historia de Usuario del proyecto

                :return: QuerySet / None
                """
        try:
            historia = historiaUsuario.objects.get(id=idHistoria)
        except historiaUsuario.DoesNotExist as e:
            print(e)
            return None

        # verificando si existe como historia de usuario del proyecto dado
        if str(historia.proyecto.id) == str(idProyecto):
            historial = historia.history.all()
            return historial
        else:
            print("La historia de usuario no pertenece al proyecto dado...")
            return None


    def obtenerHistorialUS(self, idProyecto, idHistoria, idVersion):
        """Retorna la version del historial de US, del proyecto dado, con el id idHistoria y version idVersion

                :param idProyecto: ID del proyecto
                :param idHistoria: ID de la Historia de Usuario del proyecto
                :param idVersion: ID de la version del US

                :return: QuerySet / None
                """
        try:
            historia = historiaUsuario.objects.get(id=idHistoria)
        except historiaUsuario.DoesNotExist as e:
            print(e)
            return None

        # verificando si existe como historia de usuario del proyecto dado
        if str(historia.proyecto.id) == str(idProyecto):
            versionBuscada = historia.history.filter(history_id=idVersion)
            aux = historia.history.filter(history_id=idVersion).only('nombre', 'descripcion', 'history_change_reason', 'prioridad_tecnica', 'prioridad_negocio', 'estimacion_horas', 'tipo_historia_usuario', 'desarrollador_asignado', 'proyecto', 'horas_trabajadas', 'prioridad_final', 'estado')
            versionUltima = historia.history.latest()
            diff = versionUltima.diff_against(versionBuscada[0], included_fields=('nombre', 'descripcion', 'history_change_reason', 'prioridad_tecnica', 'prioridad_negocio', 'estimacion_horas', 'tipo_historia_usuario', 'desarrollador_asignado', 'proyecto', 'horas_trabajadas', 'prioridad_final', 'estado'))

            diferencias = list()

            for cambio in diff.changes:
                diferencias.append(dict({"campo": cambio.field, "anterior": cambio.old, "actual": cambio.new}))
                #print("{} <<{}>> ==> <<{}>>".format(cambio.field, cambio.old, cambio.new))

            return [versionBuscada, diferencias]
        else:
            print("La version de la historia de usuario no existe en el proyecto dado...")
            return None


    def restaurarHistorialUS(self, idProyecto, idHistoria, idVersion, user):
        """Restaura una Historia de Usuario a una version anterior con el id de versiones dado.

        :param idProyecto: ID del proyecto
        :param idHistoria: ID de la Historia de Usuario del proyecto
        :param idVersion: ID de la Version a la cual restaurar el US
        :param user: Instancia de usuario que realiza la accion de restaurar

        :return: QuerySet / None
        """
        try:
            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print(e)
                return None

            # verificando si existe como historia de usuario del proyecto dado
            if str(historia.proyecto.id) == str(idProyecto):
                # Restauramos la version anterior
                version = historia.history.get(history_id=idVersion)
                version.instance.save()
                versionFinal = historia.history.latest()
                versionFinal.history_user = user
                versionFinal.save()



                # Problema: Desactivar crear historial cuando se add/remove de un m2m
                # Solucion temporal: Borrar todos los registros del historial que se encuentren
                # luego de la version restaurada.
                ultimaVersion = historia.history.latest()

                # Obtenemos todos los ids de actividades actuales
                queryActividades = historia.actividades.all()
                # Eliminamos
                for x in queryActividades:
                    historia.actividades.remove(x.id)

                # Guardamos en la version actual las actividades de la version restaurada.
                m2m_actividades = get_model("historiasDeUsuario_proyecto", "historicalhistoriaUsuario_actividades")
                lista = m2m_actividades.objects.filter(history_id=idVersion).values("actividadesus_id")

                # Guardamos las actividades de la version a restaurar
                for x in lista:
                   historia.actividades.add(x['actividadesus_id'])


                # Borramos las versiones posteriores
                aux1 = ultimaVersion.next_record
                while aux1 is not None:
                    # Borramos del m2m historico
                    m2m_actividades.objects.filter(history_id=aux1.history_id).delete()
                    aux2 = aux1
                    aux1 = aux1.next_record
                    # Borramos de la tabla de historica de US
                    aux2.delete()

                # Definimos el motivo del cambio
                cambiarMotivoHistorial(historia, "Restaurado")

                historia = historiaUsuario.objects.filter(id=historia.id)
                return historia
            else:
                print("La historia de usuario no pertenece al proyecto dado...")
                return None
        except Exception as e:
            print("Error al restaurar la version de una US! + " + str(e))
            return None



class managerActividadesUS(models.Manager):
    def crearActividad(self, datos, user):
        """Crear una actividad de una historia de usuario y asociar a la historia.

        :param datos: Dict. con los siguientes datos:

        - titulo: String titulo de la actividad.
        - descripcion: String descripcion de la actividad.
        - idHistoria: ID de US.
        - horasTrabajadas: Cant. de horas trabajadas en esta actividad.
        - idProyecto: ID del proyecto al que pertenece la US.
        - idSprint: ID del sprint actual al que pertenece el US.

        :param user: Instancia usuario que realiza el request.
        Debe ser el usuario actualmente asignado a la US

        :return: QuerySet / None
        """
        try:
            titulo = datos['titulo']
            descripcion = datos['descripcion']
            idHistoria = datos['idHistoria']
            horasTrabajadas = datos['horasTrabajadas']
            idProyecto = datos['idProyecto']
            idSprint = datos['idSprint']

            # Verificamos el proyecto exista
            try:
                proyecto = Proyecto.objects.get(id=idProyecto)
            except Proyecto.DoesNotExist as e:
                print("El proyecto no existe!")
                return None

            # Verificamos la historia de usuario exista
            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print("La historia de usuario no existe!")
                return None

            # Verificamos el sprint exista
            try:
                sprint = sprints.models.Sprint.objects.get(id=idSprint)
            except sprints.models.Sprint.DoesNotExist as e:
                print("El sprint no existe!")
                return None

            # Verificamos el usuario sea participante del proyecto
            try:
                part = participante.objects.get(proyecto=proyecto, usuario=user)
            except participante.DoesNotExist as e:
                print("El usuario no es participante del proyecto!")
                return None

            # Verificamos el estado del US
            if historia.estado == "finalizado" or historia.estado == "cancelado" or historia.estado == "aceptado":
                print("No puede agregarse actividad cuando el US no esta en ejecucion!")
                return None

            # Verificamos el US pertenece al sprint
            if not sprints.models.SprintBacklog.objects.filter(historiaUsuario=historia, idSprint=sprint).exists():
                print("El US no pertenece al sprint dado!")
                return None

            # Verificamos el Sprint esta en ejecucion
            if sprint.estado != "En Ejecución":
                print("El Sprint no se encuentra en ejecucion!")
                return None

            # Verificamos el usuario pertenece al sprint (como miembro de sprint)
            if not sprints.models.Sprint_Miembro_Equipo.objects.filter(usuario=user, sprint=sprint).exists():
                print("El usuario no es miembro del sprint!")
                return None

            # Verificamos el US tenga como participante asignado al usuario
            if historia.desarrollador_asignado != part:
                print("El usuario no tiene asignado la historia de usuario!")
                return None

            # Verificamos los datos de entrada son validos (titulo, descripcion, horasTrabajadas)
            if not [x for x in (titulo, descripcion, horasTrabajadas) if x is None] and int(horasTrabajadas) > 0:
                actividad = self.model(titulo=titulo,
                                       descripcion=descripcion,
                                       horasTrabajadas=horasTrabajadas,
                                       participante=part)
                # Guardamos las horas trabajadas que se menciona en la actividad
                if not historia.horas_trabajadas:
                    historia.horas_trabajadas = 0
                historia.horas_trabajadas += int(horasTrabajadas)
                actividad.save()
                historia.actividades.add(actividad)
                cambiarMotivoHistorial(historia, "Actividad Agregada")
                historia.save()
                actividad = ActividadesUS.objects.filter(id=actividad.id)
                return actividad
            else:
                return None

        except Exception as e:
            print("Error al crear actividad de historia de usuario! + " + str(e))
            return None


    def obtenerActividad(self, datos):
        """Obtener una actividad de un US

        :param datos: Dict. Con los siguientes valores:

        - idHistoria : ID de la Historia de Usuario
        - idActividad : ID de la Actividad a obtener

        :return: Boolean
        """

        try:
            idHistoria = datos['idHistoria']
            idActividad = datos['idActividad']

            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print("No existe la historia de usuario!")
                return False

            try:
                actividad = ActividadesUS.objects.get(id=idActividad)
            except ActividadesUS.DoesNotExist as e:
                print("No existe la actividad!")
                return False

            # Verificamos si existe como actividad del US y si se encuentra en desarrollo actualmente
            if historia.actividades.filter(id=actividad.id).exists():
                actividad = ActividadesUS.objects.filter(id=actividad.id)
                return actividad
            else:
                return None
        except Exception as e:
            print("Error al obtener actividad de historias de usuario! + " + str(e))
            return None

    def eliminarActividad(self, datos):
        """Elimina una actividad de un US

        :param datos: Dict. Con los siguientes valores:

        - idHistoria : ID de la Historia de Usuario
        - idActividad : ID de la Actividad a eliminar

        :return: Boolean
        """
        try:
            idHistoria = datos['idHistoria']
            idActividad = datos['idActividad']

            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print("No existe la historia de usuario!")
                return False

            try:
                actividad = ActividadesUS.objects.get(id=idActividad)
            except ActividadesUS.DoesNotExist as e:
                print("No existe la actividad!")
                return False

            # Verificamos si existe como actividad del US y si se encuentra en desarrollo actualmente
            if historia.actividades.filter(id=actividad.id).exists() and historia.estado != "aceptado" and historia.estado != "cancelado" and historia.estado != "finalizado":
                # Actualizamos las horas trabajadas
                historia.horas_trabajadas -= actividad.horasTrabajadas
                historia.actividades.remove(actividad)
                cambiarMotivoHistorial(historia, "Actividad Eliminada")
                # actividad.delete()
                return True
            else:
                return None
        except Exception as e:
            print("Error al eliminar actividad de historias de usuario! + " + str(e))
            return None


    def listarActividadesUS(self, datos):
        """

        :param datos: Dict. Los valores que contiene son:
        - idHistoria: ID de la Historia de Usuario

        :return: QuerySet / None
        """
        try:
            idHistoria = datos['idHistoria']

            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print("No existe la historia de usuario!")
                return None

            listaActividades = historia.actividades.all()

            return listaActividades
        except Exception as e:
            print("Error en listar actividades de US! + " + str(e))
            return None


class ActividadesUS(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    horasTrabajadas = models.IntegerField(null=True)
    participante = models.ForeignKey(participante, null=True, on_delete=models.SET_NULL)

    # Aceptado/Rechazado?, depende de si el eliminar es logico/fisico
    estado = models.CharField(max_length=20, null=True)

    objects = managerActividadesUS()


class historiaUsuario(models.Model):
    # Caracteristicas de la HU
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200)
    prioridad_tecnica = models.IntegerField(null=True)
    prioridad_negocio = models.IntegerField(null=True)
    estimacion_horas = models.IntegerField(null=True)
    tipo_historia_usuario = models.ForeignKey(Tipo_Historia_Usuario, null=True, on_delete=models.SET_NULL)
    desarrollador_asignado = models.ForeignKey(participante, null=True, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    horas_trabajadas = models.IntegerField(null=True)
    prioridad_final = models.IntegerField(null=True)
    estado = models.CharField(max_length=200, null=True)
    sprints_trabajados = models.IntegerField(null=True) # Cantidad de Sprints en los que se trabajó la Historia

    # Para registrar las actividades/comentarios como parte del historial de una version
    actividades = models.ManyToManyField(ActividadesUS)

    # Para registrar los cambios del historial
    history = HistoricalRecords(user_model=Usuario, m2m_fields=[actividades])

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    objects = managerHistoriaUsuario()


    # Para guardar sin registrar en el historial
    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret


    def __str__(self):
        return str([self.nombre, self.descripcion, self.prioridad_tecnica,
                    self.prioridad_negocio, self.estimacion_horas,
                    self.tipo_historia_usuario, self.desarrollador_asignado,
                    self.proyecto, self.horas_trabajadas])


def cambiarMotivoHistorial(historia, motivo):
    """Cambia el campo history_change_reason con el motivo recibido
        Este metodo se llama cuando se acaba de realizar una modificacion al US

    :param version: Instancia historial_us
    :param motivo: String, motivo del cambio

    :return: None
    """

    ultimaVersion = historia.history.latest()
    ultimaVersion.history_change_reason = motivo
    ultimaVersion.save()
