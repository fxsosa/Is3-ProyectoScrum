import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.views import APIView
from django.core import serializers

import proyectos.models
from historiasDeUsuario_proyecto.models import historiaUsuario
from usuarios.models import Usuario


class ListaHistoriasUsuario(APIView, CreateView):

    def get(self, request):

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
        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datos = body
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['idProyecto'])
            if user.has_perm('proyectos.crear_historia_usuario', obj=proyecto):
                historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos)
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
        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        datos = request.data

        try:
            proyecto = proyectos.models.Proyecto.objects.get(id=datos['idProyecto'])
            if user.has_perm('proyectos.actualizar_historia_usuario', obj=proyecto):
                historia = historiaUsuario.objects.actualizarHistoriaUsuario(datos=datos)
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

        user = validarRequest(request)
        # Obtenemos el cuerpo de la peticion
        body = request.data

        try:
            idProyecto = request.GET.get('idProyecto', '')
            proyecto = proyectos.models.Proyecto.objects.get(id=idProyecto)
            if user.has_perm('proyectos.borrar_historia_usuario', obj=proyecto):
                idHistoria = request.GET.get('idHistoria', '')
                if historiaUsuario.objects.eliminarHistoriaUsuario(idProyecto=idProyecto, idHistoria=idHistoria):
                    return HttpResponse("Historia de Usuario eliminada con exito!", status=201)
                else:
                    return HttpResponse("No se pudo eliminar la historia de usuario!", status=500)
            else:
                return HttpResponse("No se tienen los permisos para borrar historias de usuario!", status=403)
        except Exception as e:
            return HttpResponse("Error al eliminar la Historia de Usuario - " + str(e), status=500)


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