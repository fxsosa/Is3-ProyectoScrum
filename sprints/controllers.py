import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.views import APIView
from django.core import serializers

import proyectos.models
from historiasDeUsuario_proyecto.models import historiaUsuario
from sprints.models import Sprint, Sprint_Miembro_Equipo
from usuarios.models import Usuario

class controllerListarSprints(APIView):

    def get(self, request):
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

    def update(self, request):
        pass

    def delete(self, request):
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
class controllerEquipoSprint(APIView):

    # Retorna todos los miembros del equipo de un Sprint
    def get(self, request):

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