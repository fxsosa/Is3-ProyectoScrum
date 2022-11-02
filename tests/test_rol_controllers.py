import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import request
import jwt
from django.test import Client
from django.core import serializers

from proyectos.models import Proyecto, participante
from roles.models import Rol

tokenAnonymous = "Bearer " + jwt.encode(key="secret", payload={"email": "AnonymousUser",
                   "password": None,
                   "given_name": "",
                   "family_name": "",
                   "rol": None})


@pytest.mark.django_db
def test_controllerListaRoles_get():
    User = get_user_model()
    rol1 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    rol2 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    userAnonimo = User.objects.get(email="AnonymousUser")
    # Asignamos un rol y permisos de listar roles al usuario anonimo
    rol3 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="roles.listar_roles_externos")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="proyectos.listar_roles_internos")
    Rol.objects.asignarRolaUsuario(idRol=rol3.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/rol/listar?tipo=Todos')
    data = json.loads(response.content)

    # Verificamos los datos del response
    assert str([data[0]['pk'], data[1]['pk'], data[2]['pk']]) == str([rol1.id, rol2.id, rol3.id])

    # Verificamos el status del response
    assert response.status_code == 200


@pytest.mark.django_db
def test_controllerRol_get():
    User = get_user_model()
    rol1 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    userAnonimo = User.objects.get(email="AnonymousUser")
    # Asignamos un rol y permisos de listar roles al usuario anonimo
    rol3 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="roles.listar_roles_externos")
    Rol.objects.asignarRolaUsuario(idRol=rol3.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/rol/?id=' + str(rol1.id) + "&tipo=Externo")
    data = json.loads(response.content)[0]


    # Verficamos los datos del response
    assert str([data['pk'], data['fields']['nombre'], data['fields']['descripcion']]) == str([
        rol1.id, "Rol Externo", "Descripcion de Rol Externo"])

    # Verificamos el status del response
    assert response.status_code == 200, "Error al verificar el status de obtener rol"


@pytest.mark.django_db
def test_controllerRol_post():
    User = get_user_model()
    userAnonimo = User.objects.get(email="AnonymousUser")
    # Asignamos un rol y permisos de listar roles al usuario anonimo
    rol3 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="roles.crear_rol_externo")
    Rol.objects.asignarRolaUsuario(idRol=rol3.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/rol/', content_type='application/json', data={"tipo": "Externo",
                                                                                 "nombre": "Nombre Rol",
                                                                                 "descripcion": "Descripcion",
                                                                                 "permisos": []})


    data = json.loads(response.content)[0]['fields']


    # Verficamos los datos del response
    assert str([data['nombre'], data['tipo'], data['descripcion']]) == str([
        "Nombre Rol", "Externo", "Descripcion"])

    # Verificamos el status del response
    assert response.status_code == 201, "Error al verificar el status de obtener rol"


@pytest.mark.django_db
def test_controllerRol_put():
    User = get_user_model()
    rol1 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    userAnonimo = User.objects.get(email="AnonymousUser")
    # Asignamos un rol y permisos de listar roles al usuario anonimo
    rol3 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="roles.actualizar_rol_externo")
    Rol.objects.asignarRolaUsuario(idRol=rol3.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/rol/', content_type='application/json',
                     data={"id": rol1.id,
                           "accion": "agregar",
                           "tipo": "Externo",
                           "nombreNuevo": "Nombre Nuevo",
                           "descripcionNueva": "Descripcion Nueva",
                           "permisos": []})
    data = json.loads(response.content)[0]

    # Verificando los datos del response
    assert str([data['pk'], data['fields']['tipo'], data['fields']['nombre'], data['fields']['descripcion']]) == str([
        rol1.id, "Externo", "Nombre Nuevo", "Descripcion Nueva"]), "Error al actualizar rol"

    # Verificando el status del response
    assert response.status_code == 201, "Error al verificar el status del response de actualizar rol"


@pytest.mark.django_db
def test_controllerRol_delete():
    User = get_user_model()
    rol1 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    userAnonimo = User.objects.get(email="AnonymousUser")
    # Asignamos un rol y permisos de listar roles al usuario anonimo
    rol3 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="roles.borrar_rol_externo")
    Rol.objects.asignarRolaUsuario(idRol=rol3.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.delete('/api/v1/rol/?id=' + str(rol1.id) + '&tipoRol=Externo')

    data = response.content.decode("utf-8")

    # Verificando el response
    assert data == "Rol Eliminado", "Error al verificar controller de borrar rol"

    # Verificando status del response
    assert response.status_code == 200, "Error al verificar el status del response de borrar rol"


@pytest.mark.django_db
def test_controllerUsuarioRoles_get():
    tokenUsuario = "Bearer " + jwt.encode(key="secret", payload={"email": "user1@email.com",
                                                                   "password": None,
                                                                   "given_name": "Nombre1",
                                                                   "family_name": "Apellido1",
                                                                   "rol": None})

    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    rol1 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    rol2 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.asignarRolaUsuario(idRol=rol1.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rol2.id, user=user1)


    c = Client(HTTP_AUTHORIZATION=tokenUsuario)
    response = c.get('/api/v1/rol/usuario')
    data = json.loads(response.content)

    # Verificando data del response
    assert str([data[0], data[1]]) == str([str(rol1.id), str(rol2.id)]), "Error en el controller de listar roles por usuario"

    # Verificando status del response
    assert response.status_code == 200, "Error al verificar el status del response del controller de listar roles de " \
                                        "usuario"
