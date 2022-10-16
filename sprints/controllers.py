import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.views import APIView
from django.core import serializers

import proyectos.models
from historiasDeUsuario_proyecto.models import historiaUsuario
from sprints.models import Sprint, Sprint_Miembro_Equipo, SprintBacklog
from usuarios.models import Usuario

class controllerListarSprints(APIView):

    def get(self, request):
        """Metodo get para listar todos los sprints de un proyecto dado.

        :param request: Request, donde los parametros recibidos por queryParam son
        "idProyecto" para el ID del proyecto, y "idSprint" para el ID del sprint

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Procesamos el request
        try:
            idproyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idproyecto)
            if user.has_perm('proyectos.listar_sprint_proyecto', obj=proyecto):
                listaSprints = Sprint.objects.listarSprints(idProyecto=idproyecto)
                if listaSprints is not None:
                    serializer = serializers.serialize('json', listaSprints)
                    return HttpResponse(serializer, content_type='application/json', status=200)
                else:
                    return HttpResponse("No se pudieron listar los sprints del proyecto! ", status=500)
            else:
                return HttpResponse("No se tienen los permisos para listar sprints de este proyecto!", status=403)
        except Exception as e:
            return HttpResponse("No se pudieron listar los sprints! - " + str(e), status=500)


class controllerSprint(APIView):

    def post(self, request):
        """Metodo para crear un sprint de un proyecto

        :param request: Request, con request.data con los siguientes parametros:
        "idProyecto", "nombre", "descripcion", "capacidadEquipo", "cantidadDias"

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datos = body
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['idProyecto'])
            if user.has_perm('proyectos.crear_sprint', obj=proyecto):
                sprint = Sprint.objects.crearSprint(datos=datos)
                if sprint is not None:
                    # Retornar el rol creado
                    querySprint_json = serializers.serialize('json', sprint)
                    return HttpResponse(querySprint_json, content_type='application/json', status=201)
                else:
                    return HttpResponse("No se pudo registrar el sprint", status=500)
            else:
                return HttpResponse("No se tienen los permisos para crear sprints!", status=403)
        except Exception as e:
            return HttpResponse("Error al registrar sprint - " + str(e), status=500)

    def get(self, request):
        """Metodo para obtener un Sprint de un Proyecto

        :param request: Request. Los parametros del queryparam son "idProyecto" y "idSprint"

        :return: HttpResponse
        """

        user = validarRequest(request)
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_sprint', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                sprint = Sprint.objects.obtenerSprint(idProyecto=idProyecto, idSprint=idSprint)
                if sprint is not None:
                    # Convertimos a json
                    jsonRespuesta = serializers.serialize('json', sprint)
                    return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
                else:
                    return HttpResponse("No se pudo obtener el sprint! ", status=500)
            else:
                return HttpResponse("No se tienen los permisos para obtener sprints del proyecto!", status=403)
        except Exception as e:
            return HttpResponse("No se pudo obtener el sprint del proyecto! " + str(e), status=500)

    def put(self, request):
        """Metodo para actualizar un sprint de un proyecto

        :param request: Request. Los parametros del request.data son:
        "idProyecto", "idSprint", "nombre", "descripcion", "cantidadDias"

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datos = body
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['idProyecto'])
            if user.has_perm('proyectos.actualizar_sprint', obj=proyecto):
                try:
                    sprint = Sprint.objects.get(id=datos['idSprint'])
                except Sprint.DoesNotExist as e:
                    return HttpResponse("No existe el sprint! ", status=400)

                if sprint.estado == "Planificación":
                    sprintActualizado = Sprint.objects.actualizarSprint(datos)
                    if sprintActualizado is not None:
                        # Retornar el sprint actualizado
                        sprint_json = serializers.serialize('json', sprintActualizado)

                        # Crear un nuevo miembro del equipo de un Sprint
                        return HttpResponse(sprint_json, content_type='application/json', status=201)
                    else:
                        return HttpResponse("No se pudo actualizar el sprint", status=500)
                else:
                    return HttpResponse("No se puede actualizar sprints con estado \"" + str(sprint.estado) + "\"!", status=403)

            else:
                return HttpResponse("No se tienen los permisos para modificar miembros de Sprints!", status=403)
        except Exception as e:
            return HttpResponse("Error al modificar miembro de Sprint: " + str(e), status=500)

    def delete(self, request):
        """Metodo para cancelar un sprint

        :param request: Request, los parametros por queryParam son "idProyecto" y "idSprint"

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.borrar_sprint', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                if Sprint.objects.eliminarSprint(idProyecto=idProyecto, idSprint=idSprint):
                    return HttpResponse("Sprint eliminado con exito!", status=201)
                else:
                    return HttpResponse("No se pudo eliminar el sprint!", status=500)
            else:
                return HttpResponse("No se tienen los permisos para borrar sprints del proyecto!", status=403)
        except Exception as e:
            return HttpResponse("Error al eliminar el sprint - " + str(e), status=500)

# Controlador para manejar los equipos en un Sprint
class controllerEquipoSprint(APIView):

    # Retorna todos los miembros del equipo de un Sprint
    def get(self, request):
        """Metodo de para obtener todos los miembros del equipo de un sprint

        :param request: Request, recibe por queryParam "idProyecto", "idSprint"

        :return: HttpResponse
        """

        user = validarRequest(request)
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.ver_equipo_sprint', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                sprint = Sprint.objects.obtenerSprint(idProyecto=idProyecto, idSprint=idSprint)
                if sprint is not None:
                    # Convertimos a json y retornamos los miembros del equipo del Sprint
                    miembros = Sprint_Miembro_Equipo.objects.filter(sprint_id=idSprint)
                    jsonRespuesta = serializers.serialize('json', miembros)

                    return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
                else:
                    return HttpResponse("No se pudo obtener el sprint! ", status=500)
            else:
                return HttpResponse("No se tienen los permisos para obtener sprints del proyecto!", status=403)
        except Exception as e:
            return HttpResponse("No se pudo obtener el sprint del proyecto! " + str(e), status=500)

        # Añade a un usuario al equipo de un Sprint
    def post(self, request):
        """Metodo para agregar un miembro de equipo en un sprint

        :param request: Request. Recibe en el request.data los siguientes parametros:
        "proyecto_id", "capacidad", "usuario_id", "sprint_id"

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datos = body
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['proyecto_id'])
            if user.has_perm('proyectos.agregar_miembro_sprint', obj=proyecto):
                sprint = Sprint.objects.obtenerSprint(idProyecto=datos['proyecto_id'], idSprint=datos['sprint_id'])
                miembro_equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos)
                if sprint is not None:
                    # Retornar el rol creado
                    miembro_equipo_json = serializers.serialize('json', [miembro_equipo, ])

                    # Crear un nuevo miembro del equipo de un Sprint
                    return HttpResponse(miembro_equipo_json, content_type='application/json', status=201)
                else:
                    return HttpResponse("No se pudo registrar el miembro de sprint", status=500)
            else:
                return HttpResponse("No se tienen los permisos para crear miembros de Sprints!", status=403)
        except Exception as e:
            return HttpResponse("Error al registrar miembro de Sprint: " + str(e), status=500)

    def put(self, request):
        """Metodo para actualizar la capacidad de un participante de un proyecto

        :param request: Request, con el request.data con los siguientes parametros:
        "proyecto_id", "capacidad", "miembro_equipo_id"

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datos = body
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['proyecto_id'])
            if user.has_perm('proyectos.modificar_miembro_sprint', obj=proyecto):
                sprint = Sprint.objects.obtenerSprint(idProyecto=datos['proyecto_id'], idSprint=datos['sprint_id'])
                miembro_equipo = Sprint_Miembro_Equipo.objects.modificarMiembro(datos)
                if sprint is not None:
                    # Retornar el rol creado
                    miembro_equipo_json = serializers.serialize('json', [miembro_equipo, ])

                    # Crear un nuevo miembro del equipo de un Sprint
                    return HttpResponse(miembro_equipo_json, content_type='application/json', status=201)
                else:
                    return HttpResponse("No se pudo modificar el miembro de sprint", status=500)
            else:
                return HttpResponse("No se tienen los permisos para modificar miembros de Sprints!", status=403)
        except Exception as e:
            return HttpResponse("Error al modificar miembro de Sprint: " + str(e), status=500)

    def delete(self, request):
        """Metodo para eliminar un miembro de equipo de un sprint de proyecto

        :param request: Request, con los siguientes parametros en el query: "idProyecto",
        "idSprint", "idMiembroEquipo"

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.borrar_miembro_sprint', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                id_miembro_equipo = request.GET.get('idMiembroEquipo', '')
                if Sprint_Miembro_Equipo.objects.eliminarMiembro(idProyecto=idProyecto, idSprint=idSprint,
                                                                 id_miembro_equipo=id_miembro_equipo):
                    return HttpResponse("Miembro del equipo eliminado con exito!", status=201)
                else:
                    return HttpResponse("No se pudo eliminar el miembro del equipo!", status=500)
            else:
                return HttpResponse("No se tienen los permisos para borrar miembros del equipo del sprint!", status=403)
        except Exception as e:
            return HttpResponse("Error al eliminar miembro del equipo - " + str(e), status=500)

class controllerSprintBacklog(APIView):

    def get(self, request):
        """Metodo para obtener la lista de US de un Sprint Backlog

        :param request: Request. Recibe como parametros del query "idProyecto", "idSprint"

        :return: HttpResponse
        """

        user = validarRequest(request=request)
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_sprint', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                sprintBacklog = SprintBacklog.objects.listarHistoriasUsuario(proyecto_id=idProyecto, sprint_id=idSprint)
                if sprintBacklog is not None:
                    # Convertimos a json y retornamos el backlog del sprint
                    serializer = serializers.serialize('json', sprintBacklog)
                    return HttpResponse(serializer, content_type='application/json', status=200)
                else:
                    return HttpResponse("No se pudo obtener el sprint backlog! ", status=500)
            else:
                return HttpResponse("No se tienen los permisos para obtener el backlog del sprint!", status=403)
        except Exception as e:
            print("Error en el controller! " + str(e))
            return HttpResponse("No se pudo obtener el backlog del sprint! " + str(e), status=500)


    def delete(self, request):
        """Metodo para eliminar un US del sprint backlog

        :param request: Request. Recibe como parametros del query: "idProyecto",
        "idSprint", "idHistoria"

        :return:
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.borrar_historia_sprintbacklog', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                idHistoria = request.GET.get('idHistoria', '')

                if SprintBacklog.objects.eliminarHUSprintBacklog(idProyecto=idProyecto, idSprint=idSprint, idHistoria=idHistoria):
                    return HttpResponse("Eliminado del sprintbacklog con exito!", status=201)
                else:
                    return HttpResponse("No se pudo eliminar del sprintbacklog!", status=500)
            else:
                return HttpResponse("No se tienen los permisos para borrar del sprintbacklog!", status=403)
        except Exception as e:
            return HttpResponse("Error al eliminar US del sprintbacklog - " + str(e), status=500)


class controllerEstadoSprint(APIView):

    def get(self, request):
        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_sprint', obj=proyecto):
                try:
                    sprint = Sprint.objects.get(proyecto=proyecto, estado='En Ejecución')
                    jsonRespuesta = serializers.serialize('json', [sprint, ])

                    return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
                except Sprint.DoesNotExist:
                    return HttpResponse('No hay sprint en ejecucion', status=200)

        except Exception as e:
            return HttpResponse("Error al obtener sprint - " + str(e), status=500)
    def put(self, request):
        """Metodo para cambiar el estado de un sprint
        Los estados cambian en el siguiente orden: Planificacion -> En Ejecucion -> Finalizado
        Tambien se puede definir el estado del sprint como Cancelado.

        :param request: Request. Recibe como datos en el request.data:
        "idProyecto", "idSprint", "opcion" (Avanzar para pasar al siguiente estado/Cancelar para
        cancelar el proyecto)

        :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data
            try:
                proyecto = proyectos.models.Proyecto.objects.get(id=body['idProyecto'])
            except proyectos.models.Proyecto.DoesNotExist as e:
                return HttpResponse("No existe el proyecto!", status=500)

            if user.has_perm('proyectos.actualizar_sprint', obj=proyecto):
                sprintRespuesta = Sprint.objects.cambiarEstado(idProyecto=body['idProyecto'], idSprint=body['idSprint'], opcion=body['opcion'])
                if str(type(sprintRespuesta)) == "<class 'django.db.models.query.QuerySet'>":
                    # Convertimos a json
                    sprint_json = serializers.serialize('json', sprintRespuesta)
                    # Retornamos el json
                    return HttpResponse(sprint_json, content_type='application/json', status=201)
                else:
                    return HttpResponse(sprintRespuesta, status=403)
            else:
                return HttpResponse("No se tienen los permisos para modificar estado de Sprint!", status=403)
        except Exception as e:
            print("Error en el controller! " + str(e))
            return HttpResponse("No se pudo cambiar el estado del sprint! ", status=500)

class ListaHUTipo(APIView):
    def get(self, request):
        """Metodo get para obtener una lista de historias de usuario de un tipo, de un proyecto

        :param request: Request de la peticion. Contiene como queryParam idProyecto, idTipoHU

        :return: HttpResponse
        """
        user = validarRequest(request)

        # Procesamos el request
        try:
            idproyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idproyecto)
            if user.has_perm('proyectos.obtener_sprint', obj=proyecto):
                idTipoHU = request.GET.get('idTipoHU', '')
                idSprint = request.GET.get('idSprint', '')
                listaHUTipo = SprintBacklog.objects.listarHUTipo(proyecto_id=idproyecto, tipo_id=idTipoHU, sprint_id=idSprint)
                serializer = serializers.serialize('json', listaHUTipo)
                return HttpResponse(serializer, content_type='application/json', status=200)
            else:
                return HttpResponse("No se tienen los permisos para listar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("No se pudieron listar las Historias de Usuario!", status=500)


class controllerListaTipoHU(APIView):

    def get(self, request):
        """Metodo get para obtener una lista de tipos de US de un sprint

                :param request: Request de la peticion. Contiene como queryParam idProyecto, idSprint

                :return: HttpResponse

                """
        user = validarRequest(request)

        # Procesamos el request
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_sprint', obj=proyecto):
                idSprint = request.GET.get('idSprint', '')
                listaTipoHU = SprintBacklog.objects.listarTipoHUSprint(idProyecto=idProyecto, idSprint=idSprint)
                if listaTipoHU is not None:
                    serializer = serializers.serialize('json', listaTipoHU)
                    return HttpResponse(serializer, content_type='application/json', status=200)
                else:
                    return HttpResponse("No se pudieron obtener los Tipos de Historia! ", status=500)
            else:
                return HttpResponse("No se tienen los permisos para listar Tipos de Historias!", status=403)
        except Exception as e:
            return HttpResponse("No se pudieron listar los Tipos de Historia!", status=500)


def validarRequest(request):
    # Obtenemos los datos del token
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        usuarioJSON = obtenerUsuarioConToken(token)
    except Exception as e1:
        return HttpResponse("Error al manipular el token! " + str(e1), status=401)

    # Obtenemos el usuario del modelo Usuario
    try:
        user = Usuario.objects.get(email=usuarioJSON['email'])
    except Usuario.DoesNotExist as e:
        return HttpResponse("Error al verificar al usuario! - " + str(e), status=401)

    return user


def obtenerUsuarioConToken(token):
    datosUsuario={}
    decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0

    # Creamos los campos
    datosUsuario['email'] = decoded['email']
    datosUsuario['password'] = None
    datosUsuario['nombres'] = decoded['given_name']
    datosUsuario['apellidos'] = decoded['family_name']
    datosUsuario['rol'] = None
    datosUsuario['username'] = decoded['email'].split("@")[0]

    return datosUsuario