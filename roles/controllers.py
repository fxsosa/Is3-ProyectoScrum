import jwt
from django.http import HttpResponse
from django.views.generic import CreateView
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core import serializers

import roles
from roles.models import Rol
from usuarios.models import Usuario
from itertools import chain


class ListaRoles(APIView, CreateView):

    def get(self, request):
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

        # Procesamos el request
        try:
            tipo = request.GET.get('tipo', '')
            if tipo == 'Internos':
                if user.has_perm('roles.listar_roles_internos', None):
                    listaRoles = roles.models.Rol.objects.listarRolesInternos()
                else:
                    return HttpResponse("No se tienen los permisos para listar roles internos", status=403)
            elif tipo == 'Externos':
                if user.has_perm('roles.listar_roles_externos', None):
                    listaRoles = roles.models.Rol.objects.listarRolesExternos()
                else:
                    return HttpResponse("No se tienen los permisos para listar roles externos", status=403)
            elif tipo == 'Todos':
                if user.has_perm('roles.listar_roles_internos', None) and user.has_perm('soportepermisos.listar_roles_externos', None):
                    listaRoles = roles.models.Rol.objects.listarRoles()
                else:
                    return HttpResponse("No se tienen los permisos para listar todos los roles", status=403)
            else:
                return HttpResponse("Tipo de rol no definido!", status=400)

            serializer = serializers.serialize('json', listaRoles)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("No se pudieron listar los roles! - " + str(e), status=500)


# @method_decorator(login_required, name='dispatch')
class Rol(APIView, CreateView):

    def get(self, request):
        # Obtenemos los datos dle token
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

        body = request.data
        nombreRol = request.GET.get('nombreRol', '')
        try:
            idRol=request.GET.get('id', '')
            if roles.models.Rol.objects.existeRolId(id=idRol):
                # Obtenemos Rol y su lista de permisos
                rol = roles.models.Rol.objects.get(id=idRol)
                listaPermisos = roles.models.Rol.objects.listarPermisos(id=idRol)
                print("PERMISOS SSSSSSSSSSS ", listaPermisos)
                tipoRol = rol.tipo
                if tipoRol == 'Externo':
                    if not user.has_perm('roles.listar_roles_externos', None):
                        # Tipo de rol externo y el user no tiene permiso para rol externo
                        return HttpResponse("No se tiene permiso para obtener roles externos", status=403)
                elif tipoRol=='Interno':
                    if not user.has_perm('roles.listar_roles_internos', None):
                        # Tipo de rol interno y el user no tiene permiso para rol interno
                        return HttpResponse("No se tiene permiso para obtener roles internos", status=403)

                # Si el usuario tiene el tipo de permiso para el tipo de rol obtenido:
                # Juntamos los datos del rol y su lista de permisos asociados

                rolPermisos = list(chain([rol, ], listaPermisos))

                # Convertimos a json
                jsonRespuesta = serializers.serialize('json', rolPermisos)
                return HttpResponse(jsonRespuesta, content_type='application/json', status=200)
            else:
                return HttpResponse("No existe el rol buscado!" + str(idRol), status=400)
        except Exception as e:
            return HttpResponse("No se pudo obtener el rol! " + str(e), status=500)


    def post(self, request, format=None):

        # Obtenemos los datos dle token
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

        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datosRol = body
            # Crear y guardar el rol
            if datosRol['tipo'] == 'Externo':
                if user.has_perm("roles.crear_rol_externo"):
                    nuevoRol = roles.models.Rol.objects.crearRolExterno(nombre=datosRol['nombre'], descripcion=datosRol['descripcion'])
                    nuevoRol.save()
                    listaPermisos = request.data['permisos']
                    roles.models.Rol.objects.agregarListaPermisoGlobal(nuevoRol, listaPermisos)
                else:
                    return HttpResponse("No se tiene permiso para crear rol externos!", status=403)
            elif datosRol['tipo'] == 'Interno':
                if user.has_perm("roles.crear_rol_interno"):
                    nuevoRol = roles.models.Rol.objects.crearRolInterno(nombre=datosRol['nombre'], idProyecto=datosRol['idProyecto'], descripcion=datosRol['descripcion'])
                    nuevoRol.save()
                    lista = request.data['permisos']
                    listaPermisos = []
                    for p in lista:
                        listaPermisos.append({"nombre": p, "idObjeto": datosRol['idProyecto']})

                    roles.models.Rol.objects.agregarListaPermisoObjeto(nuevoRol, listaPermisos)
                else:
                    return HttpResponse("No se tiene permiso para crear rol internos!", status=403)
            else:
                return HttpResponse("El Tipo de rol \"" + datosRol['tipo'] + "\" es invalido!", status=400)

            # Retornar el rol creado
            resultadoQueryRol = roles.models.Rol.objects.filter(id=nuevoRol.id)
            queryRol_json = serializers.serialize('json', resultadoQueryRol)
            return HttpResponse(queryRol_json, content_type='application/json', status=201)
        except Exception as e:
            return HttpResponse("Error al registrar rol - " + str(e), status=500)


    def put(self, request):
        """
        Método put para actualizar un Rol
        :param request: Request
        :return: HttpResponse
        """

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

        # Obtenemos el cuerpo de la peticion
        body = request.data
        try:
            datosRol = body
            # Crear y guardar el rol
            if datosRol['tipo'] == 'Externo':
                if user.has_perm("roles.actualizar_rol_externo"):
                    try:
                        actualizarRol = roles.models.Rol.objects.get(id=datosRol['id'], tipo='Externo')
                    except roles.models.Rol.DoesNotExist as e:
                        return HttpResponse("No existe el rol externo a actualizar! " + str(e), status=400)

                    if datosRol['nombreNuevo'] != '':
                        actualizarRol.nombre = datosRol['nombreNuevo']

                    if datosRol['descripcionNueva'] != '':
                        actualizarRol.descripcion = datosRol['descripcionNueva']

                    if datosRol['permisos'] != []:
                        if datosRol['accion'] == "agregar":
                            listaPermisos = request.data['permisos']
                            roles.models.Rol.objects.agregarListaPermisoGlobal(actualizarRol, listaPermisos)
                        elif datosRol['accion'] == "eliminar":
                            listaPermisos = request.data['permisos']
                            roles.models.Rol.objects.borrarListaPermisoGlobal(actualizarRol, listaPermisos)

                    actualizarRol.save()
                else:
                    return HttpResponse("No se tiene permiso para actualizar rol externo!", status=403)
            elif datosRol['tipo'] == 'Interno':
                if user.has_perm("roles.actualizar_rol_interno"):
                    try:
                        actualizarRol = roles.models.Rol.objects.get(id=datosRol['id'], tipo='Interno')
                    except roles.models.Rol.DoesNotExist as e:
                        return HttpResponse("No existe el rol interno a actualizar! " + str(e), status=400)
                    if datosRol['nombreNuevo'] != '':
                        actualizarRol.nombre = datosRol['nombreNuevo']

                    if datosRol['descripcionNueva'] != '':
                        actualizarRol.descripcion = datosRol['descripcionNueva']

                    if datosRol['permisos'] != []:
                        if datosRol['accion'] == "agregar":
                            idProyecto = actualizarRol.proyecto.id
                            lista = request.data['permisos']
                            listaPermisos = []
                            for p in lista:
                                listaPermisos.append({"nombre": p, "idObjeto": idProyecto})

                            roles.models.Rol.objects.agregarListaPermisoObjeto(actualizarRol, listaPermisos)
                        elif datosRol['accion'] == "eliminar":
                            idProyecto = actualizarRol.proyecto.id
                            lista = request.data['permisos']
                            listaPermisos = []
                            for p in lista:
                                listaPermisos.append({"nombre": p, "idObjeto": idProyecto})

                            roles.models.Rol.objects.borrarListaPermisoObjeto(actualizarRol, listaPermisos)

                    actualizarRol.save()
                else:
                    return HttpResponse("No se tiene permiso para actualizar rol interno!", status=403)
            else:
                return HttpResponse("El Tipo de rol \"" + datosRol['tipo'] + "\" es invalido!", status=400)

            # Retornar el rol actualizado (sin los permisos)
            resultadoQueryRol = roles.models.Rol.objects.filter(id=datosRol['id'])

            queryRol_json = serializers.serialize('json', resultadoQueryRol)
            return HttpResponse(queryRol_json, content_type='application/json', status=201)
        except Exception as e:
            return HttpResponse("Error al actualizar el rol - " + str(e), status=500)

    def delete(self, request):
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

        try:
            idRol=request.GET.get('id', '')
            print(idRol)
            if roles.models.Rol.objects.existeRolId(id=idRol):
                tipoRol = request.GET.get('tipoRol', '')
                rol = roles.models.Rol.objects.get(id=idRol)
                if rol.tipo == tipoRol:
                    if tipoRol == 'Interno':
                        if not user.has_perm("roles.borrar_rol_interno"):
                            return HttpResponse("No tiene los permisos para borrar rol interno", status=400)
                    elif tipoRol == 'Externo':
                        if not user.has_perm("roles.borrar_rol_externo"):
                            return HttpResponse("No tiene los permisos para borrar rol externo", status=400)
                else:
                    # No coinciden el tipo de rol enviado con el tipo del rol hallado en la base de datos
                    return HttpResponse("Tipo de rol invalido! ", status=400)

                roles.models.Rol.objects.borrarRol(idRol=idRol)
                return HttpResponse('Rol Eliminado', status=200)
            else:
                return HttpResponse("No existe el rol buscado!" + str(idRol), status=400)
        except Exception as e:
            return HttpResponse("No se pudo obtener el rol! " + str(e), status=500)


class usuarioRoles(APIView):
    def get(self,request):
        # Obtenemos los datos del token
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            usuarioJSON = obtenerUsuarioConToken(token)
        except Exception as e1:
            return HttpResponse("Error al manipular el token! " + str(e1), status=401)

        # Obtenemos el usuario del modelo Usuario
        """
        try:
            user = Usuario.objects.get(email=usuarioJSON['email'])
        except Usuario.DoesNotExist as e:
            return HttpResponse("Error al verificar al usuario! - " + str(e), status=401)
        """

        try:
            listaIdRoles = roles.models.Rol.objects.listarRolesPorUsuario(userEmail=usuarioJSON['email'])
            print(listaIdRoles)
            listaIdRoles_json = json.dumps(listaIdRoles)
            print("listaIdRoles_json ",listaIdRoles_json)
            return HttpResponse(listaIdRoles_json, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Error al obtener el rol - " + str(e), status=500)



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