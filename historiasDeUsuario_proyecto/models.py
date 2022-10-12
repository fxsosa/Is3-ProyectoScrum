from django.db import models

import proyectos
from historiasDeUsuario.models import Tipo_Historia_Usuario
from proyectos.models import participante, Proyecto
from usuarios.models import Usuario


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
            estimacion_horas = datos['estimacion_horas']
            idTipo = datos['idTipo']
            tipoHistoria = Tipo_Historia_Usuario.objects.get(id=idTipo)
            idParticipante = datos['idParticipante'] # Participante asignado
            desarrollador = participante.objects.get(id=idParticipante)
            proyecto = Proyecto.objects.get(id=datos['idProyecto'])

            historia = self.model(nombre=nombre, descripcion=descripcion,
                                  prioridad_tecnica=prioridad_tecnica,
                                  prioridad_negocio=prioridad_negocio,
                                  estimacion_horas=estimacion_horas,
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
                    print("+++++++++++++++++++++++++++++++++++++++++ ", desarrollador)
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

                if datos['estimacion_horas'] is not None:
                    historia.estimacion_horas = datos['estimacion_horas']

                if datos['idTipo'] is not None:
                    historia.tipo_historia_usuario = tipoHistoria

                if datos['idParticipante'] is not None:
                    historia.desarrollador_asignado = desarrollador

                historia.save()

                historia = historiaUsuario.objects.filter(id=historia.id)
                return historia
            else:
                print("La historia de usuario no pertenece al proyecto dado...")
                return None

        except Exception as e:
            print(e)
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
        """Obtiene la lista completa de historias de usuario

        :param idProyecto: ID del proyecto

        :return: QuerySet / None
        """
        try:
            proyecto = Proyecto.objects.get(id=idProyecto)
        except Proyecto.DoesNotExist as e:
            print(e)
            return None

        listaHistorias = historiaUsuario.objects.filter(proyecto=idProyecto)
        return listaHistorias


class historiaUsuario(models.Model):
    # Caracteristicas de la HU
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200)
    prioridad_tecnica = models.IntegerField(null=True)
    prioridad_negocio = models.IntegerField(null=True)
    estimacion_horas = models.IntegerField(null=True)
    tipo_historia_usuario = models.ForeignKey(Tipo_Historia_Usuario, null=True, on_delete=models.SET_NULL)
    desarrollador_asignado = models.ForeignKey(participante, null=False, on_delete=models.CASCADE)
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