from django.http import HttpResponse
from rest_framework.views import APIView
import jwt
from django.contrib.auth import get_user_model
from django.core import serializers
from usuarios.models import Usuario
from roles.models import Rol
from proyectos.models import participante, Proyecto
import json

class controllerProyecto(APIView):

    def get(self, request):
        """
        Funcion REST de GET de Proyectos, para obtener una lista de proyectos a los que
        usuario dado pertenece
        :param request: Objeto request.
        El request.data tiene el siguiente formato: {"email": "example@gmail.com"}
        :return: (HttpResponse) Lista de QuerySet de Proyectos
        """
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

            listaProyectos = participante.objects.listarProyectosdeParticipante(id=idUsuario)

            print('listaProyectos', listaProyectos)


            serializer = serializers.serialize('json', listaProyectos)
            return HttpResponse(serializer, content_type='application/json', status=200)

        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


class ControllerUsuario(APIView):
    def post(self, request, format=None):
        """Funcion para generar un usuario y guardar como usuario del sistema

        :param request: Request. El request.data contiene los siguientes campos: {"email": "example@email.com", "password": "examplePassword", "nombres": "exampleNombres", "apellidos" : "exampleApellidos", "username": "exampleUsername"}
        :param format: None

        :return: (HttpResponse) QuerySet Usuario Creado
        """
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
        """Funcion para listar todos los usuarios del sistema

        :param request: Request
        :param format: None

        :return: (HttpResponse) QuerySet de Usuarios del sistema
        """
        try:
            usuarios = Usuario.objects.all()
            serializer = serializers.serialize('json', usuarios)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal "+ str(e), status=200)

    def put(self, request, format=None):
        """Funcion para actualizar datos de un usuario por parte de un admin

        :param request: Request. El request.data contiene los siguientes campos {"email": "example@email.com", "accion": "agregar/eliminar", "roles" = [idRol1, idRol2, ...]}
        :param format: None

        :return: (HttpResponse) QuerySet de Usuario actualizado / Vacio si fue eliminado
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
        """Funcion para obtener roles de un usuario por parte del admin

        :param request: Request. Se recibe como query param 'email' del usuario
        :param format: None

        :return: (HttpResponse) QuerySet de Roles
        """
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data

            # Obtenemos el token de la cabecera y decodificamos
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

            datosUsuario = obtenerUsuarioConToken(token)
            # Preguntar si ya existe el usuario



            resultadoQueryRoles = Rol.objects.listarRolesPorUsuario(userEmail=request.GET.get('email', ''))

            print('resultadoQueryRoles',resultadoQueryRoles)
            serializer = json.dumps(resultadoQueryRoles)
            return HttpResponse(serializer, content_type='application/json', status=200)

        except Exception as e:
            return HttpResponse("Algo salio mal al buscar los roles de usuarios " + str(e), status=500)

class ControllerUsuarioExistencia(APIView):
    def get(self,request):
        """Funcion para verificar si un usuario existe o no en el sistema

        :param request: Request. El query param recibido es 'email' del usuario a verificar

        :return: (HttpResponse) QuerySet de un Usuario
        """
        try:
            # Obtenemos el cuerpo de la peticion
            body = request.data

            # Obtenemos el token de la cabecera y decodificamos
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]

            datosUsuario = obtenerUsuarioConToken(token)
            # Preguntar si ya existe el usuario
            userEmail = request.GET.get('email', '')
            resultadoQueryUsuario = Usuario.objects.filter(email=userEmail)

            # retornar el usuario existente
            if resultadoQueryUsuario:
                queryUsuario_json = serializers.serialize('json', resultadoQueryUsuario)
                return HttpResponse(queryUsuario_json, content_type='application/json', status=200)
            else:
                vacio = {}
                return HttpResponse(vacio, content_type='application/json', status=200)
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
