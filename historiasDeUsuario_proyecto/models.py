from django.db import models

import proyectos

from historiasDeUsuario.models import Tipo_Historia_Usuario, Columna_Tipo_Historia_Usuario
from proyectos.models import participante, Proyecto
from usuarios.models import Usuario
from itertools import chain



class managerHistoriaUsuario(models.Manager):
    def crearHistoriaUsuario(self, datos):
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

        :return: QuerySet de Historia de Usuario Creada / None
        """

        try:
            nombre = datos['nombre']
            descripcion = datos['descripcion']
            prioridad_tecnica = datos['prioridad_tecnica']
            prioridad_negocio = datos['prioridad_negocio']

            # Agregamos prioridad_general en caso de que ya tengamos la prioridad tecnica y de negocio
            prioridad_final = None
            if prioridad_tecnica is not None and prioridad_negocio is not None:
                prioridad_final = round(0.6 * prioridad_negocio + 0.4 * prioridad_tecnica)  # Redondea el valor decimal

            estimacion_horas = datos['estimacion_horas']
            idTipo = datos['idTipo']
            if datos['idTipo']:
                tipoHistoria = Tipo_Historia_Usuario.objects.get(id=idTipo)
            else:
                tipoHistoria = None
            idParticipante = datos['idParticipante'] # Participante asignado
            if datos['idParticipante']:
                desarrollador = participante.objects.get(id=idParticipante)
            else:
                desarrollador = None
            proyecto = Proyecto.objects.get(id=datos['idProyecto'])

            historia = self.model(nombre=nombre, descripcion=descripcion,
                                  prioridad_tecnica=prioridad_tecnica,
                                  prioridad_negocio=prioridad_negocio,
                                  estimacion_horas=estimacion_horas,
                                  prioridad_final=prioridad_final,
                                  tipo_historia_usuario=tipoHistoria,
                                  desarrollador_asignado=desarrollador,
                                  proyecto=proyecto)
            historia.save()

            historia = historiaUsuario.objects.filter(id=historia.id)
            return historia
        except Exception as e:
            print(e)
            return None

    def eliminarHistoriaUsuario(self, idProyecto, idHistoria):
        """Elimina de forma lógica una Historia de Usuario

        :param datos:
        - idHistoria: ID de la Historia de Usuario,
        - idProyecto: ID del proyecto al cual pertenecera esta historia de usuario

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
                historia.save()
                return True
            else:
                print("La historia de usuario no pertenece al proyecto dado...")
                return False
        except Exception as e:
            print(e)
            return False

    def actualizarHistoriaUsuario(self, datos):
        try:
            idProyecto = datos['idProyecto']
            idHistoria = datos['idHistoria']
            try:
                historia = historiaUsuario.objects.get(id=idHistoria)
            except historiaUsuario.DoesNotExist as e:
                print(e)
                return None

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

                if datos['descripcion'] is not None:
                    historia.descripcion = datos['descripcion']

                if datos['prioridad_tecnica'] is not None:
                    historia.prioridad_tecnica = datos['prioridad_tecnica']

                if datos['prioridad_negocio'] is not None:
                    historia.prioridad_negocio = datos['prioridad_negocio']

                # Actualizamos la prioridad final en caso de que se haya actualizado alguna prioridad
                if datos['prioridad_negocio'] is not None or datos['prioridad_tecnica'] is not None:
                    if historia.prioridad_negocio is not None and historia.prioridad_tecnica is not None:
                        historia.prioridad_final = round(0.6 * historia.prioridad_negocio + 0.4 * historia.prioridad_tecnica)  # Redondea el valor decimal

                if datos['estimacion_horas'] is not None:
                    historia.estimacion_horas = datos['estimacion_horas']

                if datos['idTipo'] is not None:
                    historia.tipo_historia_usuario = tipoHistoria

                if datos['idParticipante'] is not None:
                    historia.desarrollador_asignado = desarrollador

                if datos['horas_trabajadas'] is not None:
                    historia.horas_trabajadas = datos['horas_trabajadas']

                if datos['estado'] is not None:
                    # obtenemos el tipo y su columna
                    columnaId = datos['estado']
                    if columnaId != 'cancelada':
                        try:
                            columna = Columna_Tipo_Historia_Usuario.objects.get(id=columnaId)

                            columnaOrden = columna.orden
                            cantidadCol = len(Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=historia.tipo_historia_usuario_id))

                            # verificar si se paso a la ultima columna
                            if columnaOrden == cantidadCol:
                                datos['estado'] = 'finalizada'

                            historia.estado = datos['estado']

                        except Columna_Tipo_Historia_Usuario.DoesNotExist as e:
                            historia.estado = None
                            print("No existe la columna!")
                    else:
                        historia.estado = 'cancelada'

                historia.save()

                historia = historiaUsuario.objects.filter(id=historia.id)
                return historia
            else:
                print("La historia de usuario no pertenece al proyecto dado...")
                return None

        except Exception as e:
            print("error en: ",e)
            return None

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

        # Lista de historias no finalizadas ni canceladas
        listaHistoriasRestantes = historiaUsuario.objects.filter(proyecto=idProyecto).exclude(estado__in=["cancelada", "finalizada"]).order_by("-prioridad_final")

        listaHistorias = list(chain(listaHistoriasRestantes, listaHistoriasFinalizadas, listaHistoriasCanceladas))

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

    # TODO: Agregar Sprints a todo esto (aun no es necesario para la iteracion del 26)
    # ?????

    objects = managerHistoriaUsuario()


    # TODO: Para los comentarios, se tiene que crear un modelo aparte que apunte a
    # la historia de usuario a la cual hacen referencia.

    def __str__(self):
        return str([self.nombre, self.descripcion, self.prioridad_tecnica,
                    self.prioridad_negocio, self.estimacion_horas,
                    self.tipo_historia_usuario, self.desarrollador_asignado,
                    self.proyecto, self.horas_trabajadas])