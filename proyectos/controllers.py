from django.http import HttpResponse
from rest_framework.views import APIView
from django.core import serializers
from proyectos.models import Proyecto, participante
import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.utils import json
import roles
from roles.models import Rol, permisosInternos
from usuarios.models import Usuario
from itertools import chain
from proyectos.models import participante


from proyectos.models import Proyecto

# Para proyectos individuales
class controllerProyecto(APIView):
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
            id=request.GET.get('q', '') #Recibe el parámetro "q" de la url
            proyecto = Proyecto.objects.get(id=int(id))
            #if user.has_perm('proyectos.listar_proyectos', obj=proyecto):
            serializer = serializers.serialize('json', [proyecto, ])
            return HttpResponse(serializer, content_type='application/json', status=200)
            #else:
              #  return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)




    def post(self, request):

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
            if user.has_perm('proyectos.crear_proyecto', obj=None):
                proyecto = Proyecto.objects.crearProyecto(datos)

                print("proyecto[pk]",proyecto.id)
                # agg rol Srummaster
                rolInterno = Rol.objects.crearRolInterno("Srum Master",proyecto.id)
                lista = permisosInternos
                listaPermisos = []
                for p in lista:
                    listaPermisos.append({"nombre": p, "idObjeto": proyecto.id})

                roles.models.Rol.objects.agregarListaPermisoObjeto(rolInterno, listaPermisos)

                # agg participante
                scrumMaster = Usuario.objects.get(email=datos['scrumMaster'])
                proyectoAux = Proyecto.objects.get(id=proyecto.id)
                participantea = participante.objects.model(proyecto=proyectoAux, usuario=scrumMaster)
                participantea.save()
                # asignar rol scrummaster al participante

                Rol.objects.asignarRolaUsuario(idRol=rolInterno.id, user=scrumMaster)

                return HttpResponse(proyecto, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Error al crear proyecto: " + str(e), status=500)


    def put(self, request):

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
                proyecto = Proyecto.objects.get(id=int(datos['id']))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)
            if user.has_perm('proyectos.actualizar_proyecto', obj=proyecto):
                proyecto = Proyecto.objects.modificarProyecto(datos)
                return HttpResponse(proyecto, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Error al actualizar actualizar proyecto: " + str(e), status=500)



# Para proyectos en plural
class controllerProyectos(APIView):

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
            if user.has_perm('proyectos.listar_proyectos', obj=None):
                proyectos = Proyecto.objects.all()
                serializer = serializers.serialize('json', proyectos)
                return HttpResponse(serializer, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)

        except Exception as e:
            return HttpResponse("Error al listar proyectos: " + str(e), status=500)

# Para manejo de los participantes
class controllerParticipantes(APIView):

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
            id=request.GET.get('q', '') #Recibe el parámetro "q" de la url
            try:
                particip = participante.objects.get(id=int(id))
            except participante.DoesNotExist as e:
                return HttpResponse("Error al obtener participante: " + str(e), status=400)
            if user.has_perm('participante.listar_participante', obj=particip.proyecto):
                serializer = serializers.serialize('json', [particip, ])
                return HttpResponse(serializer, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    def post(self, request):

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
                proyecto = Proyecto.objects.get(id=int(datos['idProyecto']))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)
            try:
                usuario = Usuario.objects.get(id=int(datos['idUsuario']))
            except Proyecto.DoesNotExist as e: # Corregir y ponerle "usuario" en vez de proyecto
                return HttpResponse("Usuario no existe:" + str(e), status=400)

            #if user.has_perm('participante.crear_participante', obj=proyecto):
            particip = participante.objects.crearParticipante(datos)
            return HttpResponse(particip, content_type='application/json', status=200)
            #else:
             #   return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    #TODO: Falta corregir el put
    '''
    def put(self, request):
        try:
            datos = request.data
            particip = participante.objects.modificarParticipante(datos)

            return HttpResponse(particip, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)
    '''
class ControllerProyectoParticipantes(APIView):
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
            idProyecto=request.GET.get('idproyecto', '')
            participantes = participante.objects.listarParticipantedeProyectos(idProyecto=idProyecto)
            serializer = serializers.serialize('json', participantes)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

# Controlador para iniciar un proyecto individual
class controllerProyectosInicio(APIView):
    def put(self, request):
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
                proyecto = Proyecto.objects.get(id=int(datos['id']))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)
            if user.has_perm('proyectos.iniciar_proyecto', obj=proyecto):
                proyecto = Proyecto.objects.iniciarProyecto(datos)
                return HttpResponse(proyecto, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Error al actualizar actualizar proyecto: " + str(e), status=500)


class controllerProyectosImportar(APIView):

    def post(self, request):
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
                proyectoActual = Proyecto.objects.get(id=datos['idProyectoActual'])
                proyectoExterno = Proyecto.objects.get(id=datos['idProyectoExterno'])
            except Proyecto.DoesNotExist as e:
                return HttpResponse("No existe el/los proyectos recibidos! " + str(e))

            listaRol = Proyecto.objects.importarRoles(datos)
            queryRol_json = serializers.serialize('json', listaRol)
            return HttpResponse(queryRol_json, content_type='application/json', status=201)
        except Exception as e:
            return HttpResponse("Error al importar roles de proyectos: " + str(e), status=500)

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

