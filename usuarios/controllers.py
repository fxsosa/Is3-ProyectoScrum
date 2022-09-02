from django.http import HttpResponse
from rest_framework.views import APIView
import jwt
from django.contrib.auth import get_user_model
from django.core import serializers
from usuarios.models import Usuario


class controllerUsuarios(APIView):

    def get(self, request, format=None):
        try:
            usuarios = Usuario.objects.all()
            serializer = serializers.serialize('json', usuarios)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal "+ str(e), status=200)

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
                rol=datosUsuario['rol'],
                username=datosUsuario['username'])
            user.save()

            # retornar usuario creado
            resultadoQueryUsuario = Usuario.objects.filter(email=datosUsuario['email'])
            queryUsuario_json = serializers.serialize('json', resultadoQueryUsuario)
            return HttpResponse(queryUsuario_json, content_type='application/json', status=200)

        except Exception as e:
            print(e)
            return HttpResponse("Algo salio mal " + str(e), status=500)


    def put(self, request, format=None):
        try:

            usuarioActualizado = ""
            return HttpResponse(usuarioActualizado, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)



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

