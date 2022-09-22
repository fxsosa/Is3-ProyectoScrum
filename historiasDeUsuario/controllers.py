from django.http import HttpResponse
from rest_framework.views import APIView
from django.core import serializers
import jwt
import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.utils import json
import roles
from roles.models import Rol
from usuarios.models import Usuario
from itertools import chain
from proyectos.models import Proyecto

from historiasDeUsuario.models import Tipo_Historia_Usuario, Columna_Tipo_Historia_Usuario


class controllerTipoHU(APIView):
    """
        Controlador de Tipos de Historia de Usuario
    """

    # Retorna todos los tipos de HU en la base de datos (funciona perfectamente, podría ponerse en otro controlador)

    def get(self, request):
        """
            Función para obtener todos los tipos de Historias de Usuario de un proyecto
            :param request: datos del request
            :return: HttpResponse
        """
        try:
            id = request.GET.get('idproyecto', '')
            tiposHU = Tipo_Historia_Usuario.objects.filter(proyectos__in=[id])

            serializer = serializers.serialize('json', tiposHU)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


    # El POST va a crear directamente un tipo de HU
    # con su proyecto asociado
    def post(self, request):
        """
            Función para crear un tipo de Historia de Usuario
            :param datos: datos del request
            :return: HttpResponse
        """
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

        try:
            datos = request.data
            try:
                proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)
            if user.has_perm('proyectos.crear_tipo_HU', obj=proyecto):
                tipoHU = Tipo_Historia_Usuario.objects.crearTipoHU(datos)

                return HttpResponse(tipoHU, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


    def delete(self, request):
        """
            Función para borrar un tipo de Historia de Usuario
            :param datos: datos del request
            :return: HttpResponse
        """
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

        try:
            idProyecto = request.GET.get('idproyecto', '')
            idtipoHU = request.GET.get('id', '')
            try:
                proyecto = Proyecto.objects.get(id=int(idProyecto))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)
            if user.has_perm('proyectos.borrar_tipo_HU', obj=proyecto):

                Tipo_Historia_Usuario.objects.borrarTipoHU(idtipoHU)
                return HttpResponse("Borrado exitoso", status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)


        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)



    def put(self, request):
        """
        Función para importar un Tipo de HU existente de un proyecto a otro
        :param request:
        :return:
        """

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

        try:
            datos = request.data
            proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))
            print(proyecto)
            if user.has_perm('proyectos.importar_tipo_HU', obj=proyecto):
                Tipo_Historia_Usuario.objects.importarTipoHU(datos)
                return HttpResponse("Importación exitosa", status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Error encontrado: " + str(e), status=500)


class controllerTipoHU_2(APIView):
    """
        Otro controlador para Tipos de Historia de Usuario
    """

    def get(self, request):
        """
        Función para obtener un tipo de HU con sus columnas
        :param request:
        :return:
        """

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

        try:
            idProyecto = request.GET.get('idproyecto', '')
            id=request.GET.get('id', '') #Recibe el parámetro "idproyecto" de la url
            tipo_HU = Tipo_Historia_Usuario.objects.get(id=int(id))
            print(tipo_HU)

            # Obtener todas las columnas de la HU
            columnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id)
            lista_total= []

            lista_total.append(tipo_HU)

            for elemento in columnas:
                lista_total.append(elemento)

            serializer = serializers.serialize('json', lista_total)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    def put(self,request):
        """
        Funcion para actualizar un tipo de historia de usuario
        :param request:
        :return:
        """
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

        try:

            idProyecto = request.data['idProyecto']
            proyecto = Proyecto.objects.get(id=idProyecto)

            if user.has_perm("proyectos.actualizar_tipo_HU", proyecto):

                Tipo_Historia_Usuario.objects.actualizarTipoHU(request.data)

                return HttpResponse("Se ha actualiado correctamente", status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos para actualizar tipo HU", status=400)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

class controllerColumnasTipoHU(APIView):
    def get(self, request):
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

        try:
            id_columna = request.GET.get('q', '') #Recibe el parámetro "q" de la url
            columna_tipo_HU = Columna_Tipo_Historia_Usuario.objects.get(id=int(id_columna))
            print(columna_tipo_HU)
            
            serializer = serializers.serialize('json', [columna_tipo_HU, ])
            return HttpResponse(serializer, content_type='application/json', status=200)
            
        except Exception as e:
            return HttpResponse("Error encontrado:" + str(e), status=500)

    def post(self, request):
        """
        Función para añadir una nueva columna a un tipo de HU existente
        :param request: Datos del request
        :return: HttpResponse
        """
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

        datos = request.data
        try:
            try:
                proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)

            if user.has_perm('proyectos.modificar_columnas_tipo_HU', obj=proyecto):
                Columna_Tipo_Historia_Usuario.objects.agregarColumna(datos)
                return HttpResponse("Se ha creado exitosamente la nueva columna", status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Error encontrado:" + str(e), status=500)






def obtenerUsuarioConToken(token):
    """
        Función para obtener los datos de un usuario a partir de su token
        :param token: token del usuario
        :return: datosUsuario
    """
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

