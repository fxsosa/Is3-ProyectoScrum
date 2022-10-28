from rest_framework.utils import json
from rest_framework.views import APIView
from django.core import serializers
import jwt
from django.http import HttpResponse

from historiasDeUsuario_proyecto.models import historiaUsuario
import roles
from roles.models import Rol, permisosInternos
from usuarios.models import Usuario
from proyectos.models import participante



from proyectos.models import Proyecto

# Para proyectos individuales
class controllerProyecto(APIView):
    """
        Clase para el manejo de proyectos individuales
    """
    def get(self, request):
        """
            Método para obtener un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            id=request.GET.get('q', '') #Recibe el parámetro "q" de la url
            proyecto = Proyecto.objects.get(id=int(id))
            if user.has_perm('proyectos.listar_proyectos', obj=proyecto):
                serializer = serializers.serialize('json', [proyecto, ])
                return HttpResponse(serializer, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)




    def post(self, request):
        """
            Método para crear un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)


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
        """
            Método para modificar un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)


        try:
            datos = request.data
            try:
                print('id -----------------' ,datos['id'])
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

    def delete(self, request):
        """
            Método para cancelar un proyecto (eliminación lógica)
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            print(user)
            try:
                idproyecto = request.GET.get('idProyecto', '')
                mensaje = request.GET.get('mensaje', '')
                proyecto = Proyecto.objects.get(id=int(idproyecto))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)

            if user.has_perm('proyectos.eliminar_proyecto', obj=proyecto):
                Proyecto.objects.cancelarProyecto(idproyecto, mensaje)
                return HttpResponse("Cancelación exitosa", status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Error encontrado: " + str(e), status=500)


# Para proyectos en plural
class controllerProyectos(APIView):
    """
        Controlador para Proyectos
    """
    def get(self, request):
        """
            Método para obtener todos los proyectos
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

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
    """
        Controlador para participantes
    """

    def get(self, request):
        """
            Método para obtener un participante
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            correo = request.GET.get('correo', '')
            idProyecto = request.GET.get('idProyecto', '')
            usuario = Usuario.objects.get(email=correo)
            proyecto = Proyecto.objects.get(id=idProyecto)
            try:
                particip = participante.objects.get(proyecto_id=proyecto, usuario_id=usuario)
                serializer = serializers.serialize('json', [particip, ])
                return HttpResponse(serializer, content_type='application/json', status=200)
            except participante.DoesNotExist as e:
                return HttpResponse("NoExiste", status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    def post(self, request):
        """
            Método para crear un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            datos = request.data
            try:
                proyecto = Proyecto.objects.get(id=int(datos['idProyecto']))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)
            try:
                usuario = Usuario.objects.get(id=int(datos['idUsuario']))
            except Usuario.DoesNotExist as e: # Corregir y ponerle "usuario" en vez de proyecto
                return HttpResponse("Usuario no existe:" + str(e), status=400)

            if user.has_perm('proyectos.agregar_participante', obj=proyecto):
                particip = participante.objects.crearParticipante(datos)
                return HttpResponse(particip, content_type='application/json', status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    def delete(self, request):
        """
            Método para borrar un participante del proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            print(user)
            try:
                idproyecto = request.GET.get('idproyecto', '')
                proyecto = Proyecto.objects.get(id=int(idproyecto))
            except Proyecto.DoesNotExist as e:
                return HttpResponse("Proyecto no existe:" + str(e), status=400)

            if user.has_perm('proyectos.borrar_participante', obj=proyecto):
                userBorrar = Usuario.objects.get(email=request.GET.get('email', ''))
                # verificamos si es el scrum master del proyecto
                if proyecto.scrumMaster == userBorrar:
                    return HttpResponse("No se puede eliminar al Scrum Master del proyecto", status=403)
                # verificamos que no tenga tareas asignadas
                participanteBorrar = participante.objects.get(usuario=userBorrar, proyecto=proyecto)
                esParticipante = historiaUsuario.objects.filter(desarrollador_asignado=participanteBorrar).exists()
                if esParticipante:
                    return HttpResponse("No se puede eliminar el participante porque tiene tareas designadas", status=403)

                participante.objects.borrarParticipante(participanteBorrar)
                return HttpResponse("Borrado exitoso", status=200)
            else:
                return HttpResponse("El usuario no tiene los permisos suficientes", status=403)




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
    """
        Controlador para manejar participantes de un proyecto
    """
    def get(self, request):
        """
            Método para obtener los participantes de un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            idProyecto=request.GET.get('idproyecto', '')
            participantes = participante.objects.listarParticipantedeProyectos(idProyecto=idProyecto)
            serializer = serializers.serialize('json', participantes)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)


class ControllerProyectoParticipantes2(APIView):
    """
        Controlador para manejar participantes de un proyecto
    """
    def get(self, request):
        """
            Método para obtener los participantes de un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:
            idProyecto=request.GET.get('idproyecto', '')
            participantes = participante.objects.filter(proyecto_id=idProyecto)
            serializer = serializers.serialize('json', participantes)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

# Controlador para iniciar un proyecto individual
class controllerProyectosInicio(APIView):
    """
        Controlador para iniciar un proyecto individual
    """
    def put(self, request):
        """
            Método para iniciar un proyecto
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

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
class ControllerRolesProyectosUsuarios(APIView):
    """
        Controlador para listar roles internos por usuario
    """

    def get(self, request):
        """
            Método para obtener la lista de roles internos por usuario
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        try:

            idProyecto = request.GET.get('idproyecto', '')
            email=request.GET.get('email', '')

            res = Rol.objects.listarRolesInternosPorUsuario(email, idProyecto)
            queryRol_json = serializers.serialize('json', res)
            return HttpResponse(queryRol_json, content_type='application/json', status=201)

        except Exception as e:
            return HttpResponse("Error al obtener roles internos! - " + str(e), status=500)



class controllerProyectosImportar(APIView):
    """
        Controlador para importar roles de un proyecto a otro
    """

    def post(self, request):
        """
            Método para importar roles de un proyecto a otro
            :param request: datos del request
            :return: HttpResponse
        """

        user = validarRequest(request)

        datos = request.data
        try:
            try:
                proyectoActual = Proyecto.objects.get(id=datos['idProyectoActual'])
                rol = Rol.objects.get(id=datos['idRol'])
            except Proyecto.DoesNotExist as e:
                return HttpResponse("No existe el proyectos recibido o el rol! " + str(e))

            if user.has_perm("proyectos.importar_roles_internos", obj=proyectoActual):
                rolNuevo = Proyecto.objects.importarRoles(datos)
                return HttpResponse(rolNuevo, content_type='application/json', status=201)
            else:
                return HttpResponse("No tienes permiso para importar roles internos", status=400)
        except Exception as e:
            return HttpResponse("Error al importar roles de proyectos: " + str(e), status=500)


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