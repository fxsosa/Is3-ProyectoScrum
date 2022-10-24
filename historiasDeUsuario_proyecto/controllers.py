import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.views import APIView
from django.core import serializers

import proyectos.models
from historiasDeUsuario_proyecto.models import historiaUsuario
from usuarios.models import Usuario
from proyectos.models import participante


class ListaHistoriasUsuario(APIView, CreateView):

    def get(self, request):
        """Metodo get para obtener una lista de historias de usuario de un proyecto dado

        :param request: Request de la peticion. Contiene como queryParam idProyecto

        :return: HttpResponse
        """
        user = validarRequest(request)

        # Procesamos el request
        try:
            idproyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idproyecto)
            if user.has_perm('proyectos.listar_historias_usuario', obj=proyecto):
                listaHistoriasUsuario = historiaUsuario.objects.listarHistoriasUsuario(idProyecto=idproyecto)
                serializer = serializers.serialize('json', listaHistoriasUsuario)
                return HttpResponse(serializer, content_type='application/json', status=200)
            else:
                return HttpResponse("No se tienen los permisos para listar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("No se pudieron listar las Historias de Usuario! - " + str(e), status=500)


class HistoriaUsuario(APIView, CreateView):

    def get(self, request):
        """Metodo get para obtener una historia de usuario de un proyecto dado

        :param request: Request de la peticion. Contiene como queryParam el idProyecto y idHistoria

        :return: HttpResponse
        """

        user = validarRequest(request)
        body = request.data
        try:
            idProyecto=request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_historia_usuario', obj=proyecto):
                idHistoria=request.GET.get('idHistoria', '')
                historia = historiaUsuario.objects.obtenerHistoriaUsuario(idProyecto=idProyecto, idHistoria=idHistoria)
                # Convertimos a json
                jsonRespuesta = serializers.serialize('json', historia)
                return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
            else:
                return HttpResponse("No se tienen los permisos para obtener historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("No se pudo obtener la historia de usuario! " + str(e), status=500)


    def post(self, request, format=None):
        """Metodo post para crear una historia de usuario y agregar a un proyecto

        :param request: Request de la peticion. Contiene como valores de .data los campos: idProyecto,
        nombre, descripcion, prioridad_tecnica, prioridad_negocio, estimacion_horas, idTipo, idParticipante.
        :param format: None

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datos = body
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['idProyecto'])
            if user.has_perm('proyectos.crear_historia_usuario', obj=proyecto):
                historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user)
                if historia is not None:
                    # Retornar el rol creado
                    queryRol_json = serializers.serialize('json', historia)
                    return HttpResponse(queryRol_json, content_type='application/json', status=201)
                else:
                    return HttpResponse("No se pudo registrar la historia de usuario", status=500)
            else:
                return HttpResponse("No se tienen los permisos para crear historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("Error al registrar historia de usuario - " + str(e), status=500)


    def put(self, request):
        """Metodo para actualizar una historia de usuario.

        :param request: Request de la peticion. Contiene como valores de .data los campos: idProyecto,
        nombre, descripcion, prioridad_tecnica, prioridad_negocio, estimacion_horas, idTipo, idParticipante.
        Los valores que sean null no se actualizan.

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        datos = request.data

        try:
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['idProyecto'])
            if user.has_perm('proyectos.actualizar_historia_usuario', obj=proyecto):
                historia = historiaUsuario.objects.actualizarHistoriaUsuario(datos=datos, esDev=False, user=user)
                if historia is not None:
                    queryRol_json = serializers.serialize('json', historia)
                    return HttpResponse(queryRol_json, content_type='application/json', status=201)
                else:
                    return HttpResponse("No se pudo actualizar la historia de usuario", status=500)
            else:
                historiaUsu = historiaUsuario.objects.get(id=datos['idHistoria'])
                desarrolladorSolicitante = participante.objects.get(usuario=user, proyecto=proyecto)
                if historiaUsu.desarrollador_asignado == desarrolladorSolicitante:
                    historia = historiaUsuario.objects.actualizarHistoriaUsuario(datos=datos, esDev=True, user=user)
                    if historia is not None:
                        queryRol_json = serializers.serialize('json', historia)
                        return HttpResponse(queryRol_json, content_type='application/json', status=201)
                    else:
                        return HttpResponse("No se pudo actualizar la historia de usuario", status=500)
                else:
                    return HttpResponse("No se tienen los permisos para actualizar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("Error al actualizar la Historia de Usuario - " + str(e), status=500)

    def delete(self, request):
        """Metodo de delete para borrar una historia de usuario de un proyecto.

        :param request: Request de la peticion, contiene como queryParam el valor del idProyecto, idHistoria
        a borrar

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data

        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.borrar_historia_usuario', obj=proyecto):
                idHistoria = request.GET.get('idHistoria', '')
                if historiaUsuario.objects.eliminarHistoriaUsuario(idProyecto=idProyecto, idHistoria=idHistoria, user=user):
                    return HttpResponse("Historia de Usuario eliminada con exito!", status=201)
                else:
                    return HttpResponse("No se pudo eliminar la historia de usuario!", status=500)
            else:
                return HttpResponse("No se tienen los permisos para borrar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("Error al eliminar la Historia de Usuario - " + str(e), status=500)


class controllerListarHistorialUS(APIView):

    def get(self, request):
        """Metodo get para obtener el historial de un US, de un proyecto dado

        :param request: Request de la peticion. Contiene como queryParam el idProyecto y idHistoria

        :return: HttpResponse
        """

        user = validarRequest(request)
        body = request.data
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_historia_usuario', obj=proyecto):
                idHistoria = request.GET.get('idHistoria', '')
                historial = historiaUsuario.objects.listarHistorialUS(idProyecto=idProyecto, idHistoria=idHistoria)
                # Convertimos a json
                jsonRespuesta = serializers.serialize('json', historial, fields=('nombre',
                                                                                 'descripcion',
                                                                                 'history_change_reason',
                                                                                 'prioridad_tecnica',
                                                                                 'prioridad_negocio',
                                                                                 'estimacion_horas',
                                                                                 'tipo_historia_usuario',
                                                                                 'desarrollador_asignado',
                                                                                 'proyecto',
                                                                                 'horas_trabajadas',
                                                                                 'prioridad_final',
                                                                                 'estado'))
                return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
            else:
                return HttpResponse("No se tienen los permisos para obtener historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("No se pudo obtener el historial de usuario! " + str(e), status=500)


class controllerHistorialUS(APIView):

    def get(self, request):
        """Metodo get para obtener una version anterior de un US, de un proyecto dado

                :param request: Request de la peticion. Contiene como queryParam el idProyecto y idHistoria

                :return: HttpResponse
                """

        user = validarRequest(request)
        body = request.data
        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.obtener_historia_usuario', obj=proyecto):
                idHistoria = request.GET.get('idHistoria', '')
                idVersion = request.GET.get('idVersion', '')
                version = historiaUsuario.objects.obtenerHistorialUS(idProyecto=idProyecto,
                                                                       idHistoria=idHistoria,
                                                                       idVersion=idVersion)
                # Convertimos a json
                jsonRespuesta = serializers.serialize('json', version, fields=('nombre',
                                                                               'descripcion',
                                                                               'history_change_reason',
                                                                               'prioridad_tecnica',
                                                                               'prioridad_negocio',
                                                                               'estimacion_horas',
                                                                               'tipo_historia_usuario',
                                                                               'desarrollador_asignado',
                                                                               'proyecto',
                                                                               'horas_trabajadas',
                                                                               'prioridad_final',
                                                                               'estado'))
                
                return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
            else:
                return HttpResponse("No se tienen los permisos para obtener versiones de historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("No se pudo obtener la version de la historia de usuario! " + str(e), status=500)


    def put(self, request):
        """Metodo para restaurar una version de una historia de usuario.

        :param request: Request de la peticion, contiene como queryParam el valor del idProyecto, idHistoria, idVersion
        a restaurar

        :return: HttpResponse
        """

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data

        try:
            idProyecto = body['idProyecto']
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.restaurar_historia_usuario', obj=proyecto):
                idHistoria = body['idHistoria']
                idVersion = body['idVersion']
                versionRestaurada = historiaUsuario.objects.restaurarHistorialUS(idProyecto=idProyecto,
                                                                                  idHistoria=idHistoria,
                                                                                  idVersion=idVersion,
                                                                                  user=user)
                if versionRestaurada is not None:
                    queryUS_json = serializers.serialize('json', versionRestaurada, fields=('nombre',
                                                                                            'descripcion',
                                                                                            'history_change_reason',
                                                                                            'prioridad_tecnica',
                                                                                            'prioridad_negocio',
                                                                                            'estimacion_horas',
                                                                                            'tipo_historia_usuario',
                                                                                            'desarrollador_asignado',
                                                                                            'proyecto',
                                                                                            'horas_trabajadas',
                                                                                            'prioridad_final',
                                                                                            'estado'))
                    return HttpResponse(queryUS_json, content_type='application/json', status=201)
                else:
                    return HttpResponse("No se pudo restaurar la historia de usuario", status=500)
            else:
                return HttpResponse("No se tienen los permisos para restaurar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("Error al restaurar la Historia de Usuario - " + str(e), status=500)


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
            if user.has_perm('proyectos.listar_historias_usuario', obj=proyecto):
                idTipo = request.GET.get('idTipoHU', '')
                listaHUTipo = historiaUsuario.objects.listarHUTipo(idProyecto=idproyecto, idTipoHU=idTipo)
                serializer = serializers.serialize('json', listaHUTipo)
                return HttpResponse(serializer, content_type='application/json', status=200)
            else:
                return HttpResponse("No se tienen los permisos para listar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("No se pudieron listar las Historias de Usuario!", status=500)


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