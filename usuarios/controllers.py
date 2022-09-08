from django.http import HttpResponse
from rest_framework.views import APIView
import jwt
from django.contrib.auth import get_user_model
from django.core import serializers
from usuarios.models import Usuario
from roles.models import Rol
from proyectos.models import Participante, Proyecto
import json

class controllerProyecto(APIView):

    def get(self, request):
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data

            # Obtenemos el token de la cabecera y decodificamos
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

            datosUsuario = obtenerUsuarioConToken(token)
            # Preguntar si ya existe el usuario y obtenemos la id
            resultadoQueryUsuario = Usuario.objects.filter(email=datosUsuario['email']).values('id')
            idUsuario = resultadoQueryUsuario[0]
            idUsuario = idUsuario['id']

            listaProyectos = Participante.objects.listarProyectosdeParticipante(id=idUsuario)

            print('listaProyectos', listaProyectos)


            serializer = serializers.serialize('json', listaProyectos)
            print("serializer",serializer)
            return HttpResponse(serializer, content_type='application/json', status=200)

        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)




class ControllerUsuario(APIView):
    def post(self, request, format=None):
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data

            # Obtenemos el token de la cabecera y decodificamos
            token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]

            datosUsuario = obtenerUsuarioConToken(token)
            # Preguntar si ya existe el usuario
            resultadoQueryUsuario = Usuario.objects.filter(email=datosUsuario['email'])

            # retornar el usuario existente
            if resultadoQueryUsuario:
                queryUsuario_json = serializers.serialize('json', resultadoQueryUsuario)
                return HttpResponse(queryUsuario_json, content_type='application/json', status=200)

            # crear usuario
            UserMan = get_user_model()
            user = UserMan.objects.create_user(
                datosUsuario['email'],
                password=datosUsuario['password'],
                nombres=datosUsuario['nombres'],
                apellidos=datosUsuario['apellidos'],
                username=datosUsuario['username'])
            user.save()

            # retornar usuario creado
            resultadoQueryUsuario = Usuario.objects.filter(email=datosUsuario['email'])
            queryUsuario_json = serializers.serialize('json', resultadoQueryUsuario)
            return HttpResponse(queryUsuario_json, content_type='application/json', status=200)

        except Exception as e:
            print(e)
            return HttpResponse("Algo salio mal " + str(e), status=500)


class ControllerUsuarioAdministracion(APIView):
    def get(self, request, format=None):
        """
        Funcion para listar todos los usuarios del sistema
        :param request:
        :param format:
        :return:
        """
        try:
            usuarios = Usuario.objects.all()
            serializer = serializers.serialize('json', usuarios)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal "+ str(e), status=200)

    def put(self, request, format=None):
        """
        Funcion para actualizar datos de un usuario por parte de un admin
        :param request:
        :param format:
        :return:
        """
        try:
            body = request.data
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            datosUsuario = obtenerUsuarioConToken(token)
            try:
                usuarioSolicitante = Usuario.objects.get(email=datosUsuario['email'])
            except Exception as e:
                return HttpResponse("Algo salio mal al buscar el usuario " + str(e), status=500)

            """
            if not usuarioSolicitante.has_perm('usuarios.modificar_roles_externos_de_usuario', None):
                return HttpResponse("No tienes los permisos para cambiar roles externos", status=400)
            """

            usuario = Usuario.objects.get(email=body['email'])

            if body['accion'] == 'agregar':
                if body['roles']:
                    for idRol in body['roles']:
                        Rol.objects.asignarRolaUsuario(idRol=idRol, user=usuario)
            elif body['accion'] == 'eliminar':
                print("Entro elif")
                if body['roles']:
                    for idRol in body['roles']:
                        Rol.objects.eliminarRolaUsuario(idRol=idRol, user=usuario)

            resultadoQueryUsuario = Usuario.objects.filter(email=body['email'])
            queryUsuario_json = serializers.serialize('json', resultadoQueryUsuario)
            return HttpResponse(queryUsuario_json, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)




class ControllerUsuarioIndividualAdmin(APIView):
    def get(self,request):
        """
                Funcion para obtener roles de un usuario por parte del admin
                :param request:
                :param format:
                :return:
                """
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data

            # Obtenemos el token de la cabecera y decodificamos
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

            datosUsuario = obtenerUsuarioConToken(token)
            # Preguntar si ya existe el usuario
            resultadoQueryRoles = Rol.objects.listarRolesPorUsuario(userEmail=body['email'])

            print('resultadoQueryRoles',resultadoQueryRoles)
            serializer = json.dumps(resultadoQueryRoles)
            return HttpResponse(serializer, content_type='application/json', status=200)

        except Exception as e:
            return HttpResponse("Algo salio mal al buscar los roles de usuarios " + str(e), status=500)


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

