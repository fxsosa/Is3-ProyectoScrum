from django.http import HttpResponse
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core import serializers
from roles.models import Rol



class ListaRoles(APIView):

    def get(self, request):
        try:
            listaRoles = Rol.objects.listarRoles()
            serializer = serializers.serialize('json', listaRoles)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("No se pudieron listar los roles! - " + str(e), status=200)


class CrearRol(APIView):

    def post(self, request, format=None):
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data
            datosRol = body
            # retornar el rol existente
            if Rol.objects.existeRol(nombreRol=datosRol['nombre']):
                resultadoQueryRol = Rol.objects.filter(nombre=datosRol['nombre'])
                print("Buscamos por el nombre: " + datosRol['nombre'])
                queryRol_json = serializers.serialize('json', resultadoQueryRol)
                return HttpResponse(queryRol_json, content_type='application/json', status=200)
            else:
                # Crear y guardar el rol
                if datosRol['tipo'] == 'Interno':
                    nuevoRol = Rol.objects.crearRolInterno(nombre=datosRol['nombre'], descripcion=datosRol['descripcion'])
                    nuevoRol.save()
                elif datosRol['tipo'] == 'Externo':
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

    def put(self, request):
        try:
            usuarioActualizado = ""
            return HttpResponse(usuarioActualizado, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


def obtenerRol(requestJSON):
    datosRol={}
    datosRol = json.loads(requestJSON)

    return datosRol