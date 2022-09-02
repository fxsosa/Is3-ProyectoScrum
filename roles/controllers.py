import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.decorators import permission_classes
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core import serializers
from roles.models import Rol
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from guardian.shortcuts import get_perms
from usuarios.models import Usuario


class ListaRoles(APIView, CreateView):

#    @method_decorator(permission_required('soportepermisos.listar_roles'))
    def get(self, request):
        try:
            print(request)
            tipo = request.data['tipo']
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            usuarioJSON = obtenerUsuarioConToken(token)
            user = Usuario.objects.get(email=usuarioJSON['email'])

            if tipo == 'Internos':

                if user.has_perm('soportepermisos.listar_roles_internos', None):
                    listaRoles = Rol.objects.listarRolesInternos()
                    print("AAA")
                else:
                    return HttpResponse("No se tienen los permisos para listar roles internos", status=404)
            elif tipo == 'Externos':
                if 'soportepermisos.listar_roles_internos' in get_perms(user, obj=None):
                    listaRoles = Rol.objects.listarRolesExternos()
                else:
                    return HttpResponse("No se tienen los permisos para listar roles externos", status=404)
            elif tipo == 'Todos':
                if user.has_perm('soportepermisos.listar_roles_internos', None) and user.has_perm('soportepermisos.listar_roles_externos', None):
                    listaRoles = Rol.objects.listarRoles()
                else:
                    return HttpResponse("No se tienen los permisos para listar todos los roles", status=404)
            else:
                return HttpResponse("Tipo de rol no definido!", status=403)

            serializer = serializers.serialize('json', listaRoles)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("No se pudieron listar los roles! - " + str(e), status=200)


@method_decorator(login_required, name='dispatch')
class RolExterno(APIView, CreateView):

    @method_decorator(permission_required('soportepermisos.crear_rol_externo'))
    def post(self, request, format=None):
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data

            datosRol = body
            # retornar el rol existente
            if Rol.objects.existeRol(nombreRol=datosRol['nombre']):
                resultadoQueryRol = Rol.objects.filter(nombre=datosRol['nombre'])
                queryRol_json = serializers.serialize('json', resultadoQueryRol)
                return HttpResponse(queryRol_json, content_type='application/json', status=200)
            else:
                # Crear y guardar el rol
                if datosRol['tipo'] == 'Externo':
                    nuevoRol = Rol.objects.crearRolExterno(nombre=datosRol['nombre'], descripcion=datosRol['descripcion'])
                    nuevoRol.save()
                else:
                    return HttpResponse("El Tipo de rol \"" + datosRol['tipo'] + "\" es invalido!", status=500)

            # Retornar el rol creado
            resultadoQueryRol = Rol.objects.filter(nombre=datosRol['nombre'])
            queryRol_json = serializers.serialize('json', resultadoQueryRol)
            return HttpResponse(queryRol_json, content_type='application/json', status=200)

        except Exception as e:
            print(e)
            return HttpResponse("Error al registrar rol - " + str(e), status=500)

    @method_decorator(permission_required('soportepermisos.actualizar_rol_externo'))
    def put(self, request):
        try:
            usuarioActualizado = ""
            return HttpResponse(usuarioActualizado, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


@method_decorator(login_required, name='dispatch')
class RolInterno(APIView, CreateView):

    @method_decorator(permission_required('soportepermisos.crear_rol_interno'))
    def post(self, request, format=None):
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data
            datosRol = body
            # retornar el rol existente
            if Rol.objects.existeRol(nombreRol=datosRol['nombre']):
                resultadoQueryRol = Rol.objects.filter(nombre=datosRol['nombre'])
                queryRol_json = serializers.serialize('json', resultadoQueryRol)
                return HttpResponse(queryRol_json, content_type='application/json', status=200)
            else:
                # Crear y guardar el rol
                if datosRol['tipo'] == 'Interno':
                    nuevoRol = Rol.objects.crearRolInterno(nombre=datosRol['nombre'], descripcion=datosRol['descripcion'])
                    nuevoRol.save()
                else:
                    return HttpResponse("El Tipo de rol \"" + datosRol['tipo'] + "\" es invalido!", status=500)

            # Retornar el rol creado
            resultadoQueryRol = Rol.objects.filter(nombre=datosRol['nombre'])
            queryRol_json = serializers.serialize('json', resultadoQueryRol)
            return HttpResponse(queryRol_json, content_type='application/json', status=200)

        except Exception as e:
            print(e)
            return HttpResponse("Error al registrar rol - " + str(e), status=500)

    @method_decorator(permission_required('soportepermisos.actualizar_rol_interno'))
    def put(self, request):
        try:
            usuarioActualizado = ""
            return HttpResponse(usuarioActualizado, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


def obtenerJSON(requestJSON):
    datosJSON={}
    datosJSON = json.loads(requestJSON)

    return datosJSON

def obtenerUsuarioConToken(token):
    datosUsuario={}
    decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
    print(decoded)

    # Verificamos la validez del token

    # Creamos los campos
    datosUsuario['email'] = decoded['email']
    datosUsuario['password'] = None
    datosUsuario['nombres'] = decoded['given_name']
    datosUsuario['apellidos'] = decoded['family_name']
    datosUsuario['rol'] = None
    datosUsuario['username'] = decoded['email'].split("@")[0]

    return datosUsuario