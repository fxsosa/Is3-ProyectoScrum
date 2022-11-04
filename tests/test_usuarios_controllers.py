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
def test_controllerUsuarioExistencia_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/usuario/existe?email=user@email.com')

    data = json.loads(response.content)[0]['fields']

    # Verificamos los datos del usuario
    assert str([data['email'],
                data['username'],
                data['nombres'],
                data['apellidos']]) == str(['user@email.com',
                                                     'username1',
                                                     'Nombre1 Nombre2',
                                                     'Apellido1 Apellido2']), "Error en los datos del body recibido"

    # Verificamos el mensaje de status
    assert response.status_code == 200, "El email solicitado no existe asociado a un usuario"

@pytest.mark.django_db
def test_controllerUsuarioIndividualAdmin_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2')

    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    Rol.objects.asignarRolaUsuario(idRol=rolInterno.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rolExterno.id, user=user1)


    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/usuario/admin/roles?email=user@email.com')

    data = json.loads(response.content)

    # Verificamos los datos del response
    assert str(data) == str([str(rolInterno.id), str(rolExterno.id)]), "Error al listar roles de un usuario"

    # Verificamos el codigo de estatus
    assert response.status_code == 200, "Error al verificar el codigo de estatus del response"


@pytest.mark.django_db
def test_controllerUsuarioAdministracion_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')

    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/usuario/admin')

    data = json.loads(response.content)
    print("Data es:")
    print(data)

    # Verificamos los datos del response
    # Ignoramos el data[0], porque es el usuario anonimo por defecto
    assert str([data[1]['pk'], data[1]['fields']['email'], data[1]['fields']['username'],
               data[2]['pk'], data[2]['fields']['email'], data[2]['fields']['username']]) == str([
        user1.id, "user1@email.com", "username1",
        user2.id, "user2@email.com", "username2"]), "Error al listar todos los usuarios del sistema"

    # Verificamos el estatus del response
    assert response.status_code == 200, "Error al verificar el estatus del response"


@pytest.mark.django_db
def test_controllerUsuarioAdministracion_put():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')

    userAnonimo = User.objects.get(email="AnonymousUser")
    rol1 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    rol2 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")

    # Asignamos un rol y permisos de actualizar_usuario al usuario anonimo
    rol3 = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol3.id, nombrePermiso="roles.actualizar_rol_externo")
    Rol.objects.asignarRolaUsuario(idRol=rol3.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/usuario/admin', content_type='application/json', data={"email": "user1@email.com", "accion": "agregar", "roles": [rol1.id, rol2.id]})
    data = json.loads(response.content)

    # Verificamos los datos actualizados
    listaRol = Rol.objects.listarRolesPorUsuario(userEmail='user1@email.com')
    assert str([listaRol[0], listaRol[1]]) == \
           str([str(rol1.id), str(rol2.id)]), "Error al actualizar el rol de un usuario"

    # Verificamos el estatus del response
    assert  response.status_code == 200, "Error al verificar el response estatus"


@pytest.mark.django_db
def test_controllerUsuario_post():
    tokenUsuario = "Bearer " + jwt.encode(key="secret", payload={"email": "user1@email.com",
                                                                   "password": None,
                                                                   "given_name": "Nombre Prueba",
                                                                   "family_name": "Apellido Prueba",
                                                                   "rol": None})
    c = Client(HTTP_AUTHORIZATION=tokenUsuario)
    response = c.post('/api/v1/usuario/', content_type='application/json')
    data = json.loads(response.content)[0]['fields']

    # Verificamos que retorne el usuario creado
    assert str([data['email'], data['nombres'], data['apellidos'], data['username']]) == str([
        "user1@email.com", "Nombre Prueba", "Apellido Prueba", "user1"])

    # Verificamos el status del response
    assert response.status_code == 200


@pytest.mark.django_db
def test_controllerProyecto_get():
    tokenUsuario = "Bearer " + jwt.encode(key="secret", payload={"email": "user2@email.com",
                                                                 "password": None,
                                                                 "given_name": "Nombre2",
                                                                 "family_name": "Apellido2",
                                                                 "rol": None})


    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre2', apellidos='Apellido2')

    proyectoPrueba1 = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    proyectoPrueba2 = Proyecto.objects.create(nombre='Proyecto 2', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')

    # Agregamos al usuario 2 a los proyectos
    participante.objects.crearParticipante(datos={"idProyecto": proyectoPrueba1.id, "idUsuario": user2.id})
    participante.objects.crearParticipante(datos={"idProyecto": proyectoPrueba2.id, "idUsuario": user2.id})

    # Hacemos el request
    c = Client(HTTP_AUTHORIZATION=tokenUsuario)
    response = c.get('/api/v1/usuario/proyectos')

    data = json.loads(response.content)
    print("Data es:")
    print(data)

    # Verificamos los datos del response
    assert str([data[0]['pk'], data[1]['pk']]) == str([proyectoPrueba1.id, proyectoPrueba2.id]), \
        "Error en controller de listar proyectos por usuario"

    # Verificamos el status del response
    assert response.status_code == 200, \
        "Error al verificar el status del controller de listar proyectos por usuario"