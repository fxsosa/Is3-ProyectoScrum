import json
import ast
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
def test_controllerProyecto_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    # Creamos el proyecto de prueba
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.listar_proyectos", objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/proyecto/?q=' + str(proyectoPrueba.id))

    data = json.loads(response.content)[0]
    print("Data es:")
    print(data)

    # Verificando datos del response
    assert str([data['pk'], data['fields']['nombre'], data['fields']['descripcion'],
                data['fields']['fechaInicio'], data['fields']['fechaFin'],
                data['fields']['estado'], data['fields']['scrumMaster']]) == str([
        proyectoPrueba.id, "Proyecto 1", "Descripcion 1", None, None, "Creado", user1.id]), \
        "Error en el controller para obtener un proyecto"

    # Verificando status del response
    assert response.status_code == 200, "Error al verificar el status del controller para obtener un proyecto"


@pytest.mark.django_db
def test_controllerProyecto_post():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2')

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol.id, nombrePermiso="proyectos.crear_proyecto")
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/proyecto/', content_type='application/json',
                      data={"nombre": "Proyecto 1", "descripcion": "Descripcion 1",
                            "fechaInicio": None, "fechaFin": None,
                            "scrumMaster": "user@email.com"})

    # Convertimos de bytes a string, y de string a list
    data = ast.literal_eval(response.content.decode("utf-8"))

    # Verificar los datos del response
    assert str([data[0], data[1], data[2], data[3],
                data[4], data[5]]) == str(["Proyecto 1", "Descripcion 1",
                                                              None, None, user1.id, 'planificación']), \
        "Error en controller de crear proyecto"

    # Verificar el status del response
    assert response.status_code == 200, "Error al verificar el status del response del controller crear proyecto"


@pytest.mark.django_db
def test_controllerProyecto_put():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    # Creamos el proyecto de prueba
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.actualizar_proyecto", objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/proyecto/', content_type='application/json',
                      data={"id": proyectoPrueba.id, "nombre": "Nombre Actualizado", "descripcion": "Descripcion Actualizada"})

    # Convertimos de bytes a string, y de string a list
    data = ast.literal_eval(response.content.decode("utf-8"))

    # Verificar los datos del response
    assert str([data[0], data[1], data[2], data[3],
                data[4], data[5]]) == str(["Nombre Actualizado", "Descripcion Actualizada",
                                           None, None, user1.id, 'Creado']), \
        "Error en controller de actualizar proyecto"

    # Verificar el status del response
    assert response.status_code == 200, "Error al verificar el status del response del controller actualizar proyecto"


@pytest.mark.django_db
def test_controllerProyectos_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    # Creamos el proyectos de prueba
    proyectoPrueba1 = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    proyectoPrueba2 = Proyecto.objects.create(nombre='Proyecto 2', descripcion='Descripcion 2', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoGlobal(idRol=rol.id, nombrePermiso="proyectos.listar_proyectos")
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/proyectos/')

    data = json.loads(response.content)

    # Verificando los datos del response
    assert str([data[0]['pk'], data[0]['fields']['nombre'], data[0]['fields']['descripcion'],
                data[1]['pk'], data[1]['fields']['nombre'], data[1]['fields']['descripcion']]) == str([
        proyectoPrueba1.id, "Proyecto 1", "Descripcion 1",
        proyectoPrueba2.id, "Proyecto 2", "Descripcion 2"
    ]), "Error en el controller de listar todos los proyectos del sistema"

    # Verificando el status del response
    assert response.status_code == 200, "Error al verificar el status del controller de listar todos los proyectos"


@pytest.mark.django_db
def test_controllerParticipantes_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')

    # Creamos el proyectos de prueba
    proyectoPrueba1 = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')

    # Agregamos participante al proyecto
    part = participante.objects.crearParticipante(datos={"idProyecto": proyectoPrueba1.id, "idUsuario": user2.id})

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/proyecto/participante?idProyecto=' + str(proyectoPrueba1.id) + "&correo=user2@email.com")

    data = json.loads(response.content)[0]
    print("Data es:")
    print(data)

    # Verificando los datos del response
    assert str([data['pk'], data['fields']['proyecto'], data['fields']['usuario']]) == str([
        part.id, proyectoPrueba1.id, user2.id]), "Error en el controller de obtener un participante de un proyecto"

    # Verificando el status del response
    assert response.status_code == 200, "Error al verificar el status del controller de obtener participante"


@pytest.mark.django_db
def test_controllerParticipantes_post():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2')
    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')
    # Creamos el proyectos de prueba
    proyectoPrueba1 = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Externo", idProyecto=proyectoPrueba1.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.agregar_participante", objeto=proyectoPrueba1)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/proyecto/participante', content_type='application/json',
                      data={"idProyecto": proyectoPrueba1.id, "idUsuario": user2.id})

    # Convertimos a string y luego a list
    data = response.content.decode("utf-8")
    data1 = data[data.index(": ")+1:data.index(">, ")]
    data2 = data[data.index("<Usuario: ")+9:data.index(">]")]
    data1 = ast.literal_eval(data1)
    data2 = ast.literal_eval(data2)
    data = data1 + data2

    # Verificando datos del response
    # Debe contener la siguiente informacion:
    # [proyectoPrueba.nombre, proyectoPrueba.descripcion, proyectoPrueba.fechaInicio, proyectoPrueba.fechaFin,
    # proyectoPrueba.scrumMaster.id, proyectoPrueba.estado, user2.email, user2.username, user2.nombres,
    # user2.apellidos]
    assert str(data) == str([
        "Proyecto 1", "Descripcion 1", None, None, user1.id, "Creado",
    "user2@email.com", "username2", "Nombre2", "Apellido2"]), \
        "Error en el controller de agregar participante a un proyecto"

    # Verificando status del response
    assert response.status_code == 200, "Error al verificar status de controller de agregar participante"

@pytest.mark.django_db
def test_controllerParticipantes_delete():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')

    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')

    # Creamos el proyectos de prueba
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')
    # Agregamos participante al proyecto
    part = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id, "idUsuario": user2.id})

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno",
                                      idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.borrar_participante", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.delete('/api/v1/proyecto/participante?idproyecto='+ str(proyecto.id) +'&email=' + str(user2.email))

    data = response.content.decode("utf-8")

    # Verificamos los datos del response
    assert data == "Borrado exitoso", "Error en el controller de borrar participante de proyecto"

    # Verificamos el status del response
    assert response.status_code == 200, "Error al verificar el status del controller de borrar participante"


@pytest.mark.django_db
def test_controllerProyectoParticipantes_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')

    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')
    user3 = User.objects.create_user(email='user3@email.com', password='abcdefg', username='username3',
                                     nombres='Nombre3', apellidos='Apellido3')
    # Creamos el proyectos de prueba
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                       fechaFin=None, scrumMaster=user1, estado='Creado')
    # Agregamos participante al proyecto
    part = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id, "idUsuario": user2.id})
    part = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id, "idUsuario": user3.id})

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/proyecto/listar-participantes?idproyecto=' + str(proyecto.id))

    data = json.loads(response.content)

    # Verificar datos del response
    assert str([data[0]['pk'], data[1]['pk']]) == str([user2.id, user3.id]), \
        "Error en controller de listar usuarios participantes de un proyecto"

    # Verificar status del response
    assert response.status_code == 200, "Error al verificar status del response en controller de listar participantes"



@pytest.mark.django_db
def test_controllerProyectoParticipantes2_get():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')

    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')
    user3 = User.objects.create_user(email='user3@email.com', password='abcdefg', username='username3',
                                     nombres='Nombre3', apellidos='Apellido3')
    # Creamos el proyectos de prueba
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                       fechaFin=None, scrumMaster=user1, estado='Creado')
    # Agregamos participante al proyecto
    part1 = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id, "idUsuario": user2.id})
    part2 = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id, "idUsuario": user3.id})

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/proyecto/listar-participantes-id?idproyecto=' + str(proyecto.id))

    data = json.loads(response.content)
    print("Data es: ")
    print(data)

    # Verificar datos del response
    assert str([data[0]['pk'], data[1]['pk']]) == str([part1.id, part2.id]), \
        "Error en controller de listar id de participantes de un proyecto"

    # Verificar status del response
    assert response.status_code == 200, "Error al verificar status del response en controller de listar participantes"


@pytest.mark.django_db
def test_controllerProyectosInicio_put():
    # Creamos el usuario con los datos de prueba
    User = get_user_model()
    user1 = User.objects.create_user(email='user1@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1', apellidos='Apellido1')
    # Creamos el proyecto de prueba
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.iniciar_proyecto", objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/proyecto/iniciarProyecto', content_type='application/json',
                     data={"id": proyectoPrueba.id})

    # Convertimos de bytes a string, y de string a list
    data = response.content.decode("utf-8")
    print(data)
    data = data[0:data.index(' datetime')-1:] + data[data.index('),')+1:]
    data = ast.literal_eval(data)

    # Verificar los datos del response
    assert str([data[0], data[1], data[2],
                data[3], data[4]]) == str(["Proyecto 1", "Descripcion 1",
                                           None, user1.id, 'iniciado'])

    # Verificar el status del response
    assert response.status_code == 200, "Error al verificar el status del response del controller iniciar proyecto"


@pytest.mark.django_db
def test_controllerRolesProyectosUsuarios_get():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2')
    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')
    # Creamos el proyectos de prueba
    proyectoPrueba1 = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos el rol y asignamos al usuario anonimo
    rol1 = Rol.objects.crearRolInterno(nombre="Rol Interno 1", descripcion="Descripcion de Rol Interno 1", idProyecto=proyectoPrueba1.id)
    rol2 = Rol.objects.crearRolInterno(nombre="Rol Interno 2", descripcion="Descripcion de Rol Interno 2", idProyecto=proyectoPrueba1.id)
    Rol.objects.asignarRolaUsuario(idRol=rol1.id, user=user2)
    Rol.objects.asignarRolaUsuario(idRol=rol2.id, user=user2)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/proyecto/usuario/roles-internos?idproyecto' + str(proyectoPrueba1.id) +
                     '&email=user2@email.com')

    print("Response content")
    print(response.content)
    data = response.content.decode("utf-8")
    data = ast.literal_eval(data)
    print("Data es: ")
    print(data)

    # Verificamos datos del response
    assert str([data[0], data[1]]) == str([str(rol1.id), str(rol2.id)]), \
        "Error en controller de listar roles por usuario dentro de un proyecto"

    # Verificamos el status del response
    assert response.status_code == 201, \
        "Error al verificar el status del controller de listar roles internos de un usuario"


@pytest.mark.django_db
def test_controllerProyectosImportar_post():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2')
    user2 = User.objects.create_user(email='user2@email.com', password='abcdefg', username='username2',
                                     nombres='Nombre2', apellidos='Apellido2')

    # Creamos el proyectos de prueba
    proyectoPrueba1 = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')

    proyectoPrueba2 = Proyecto.objects.create(nombre='Proyecto 2', descripcion='Descripcion 2', fechaInicio=None,
                                              fechaFin=None, scrumMaster=user1, estado='Creado')

    # Creamos los roles a importar
    rol1 = Rol.objects.crearRolInterno(nombre="Rol Interno 1", descripcion="Descripcion 1",
                                      idProyecto=proyectoPrueba1.id)


    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol2 = Rol.objects.crearRolInterno(nombre="Rol Interno 2", descripcion="Descripcion 2",
                                      idProyecto=proyectoPrueba1.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol2.id, nombrePermiso="proyectos.importar_roles_internos",
                                       objeto=proyectoPrueba2)
    Rol.objects.asignarRolaUsuario(idRol=rol2.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/proyecto/importar_roles', content_type='application/json',
                      data={"idProyectoActual": proyectoPrueba2.id,
                            "idRol": rol1.id,
                            "idProyectoExterno": proyectoPrueba1.id})

    print("Response content")
    print(response.content)
    data = response.content.decode("utf-8")
    data = ast.literal_eval(data)
    print("Data es:")
    print(data)

    # Verificamos datos del response (un rol, con mismos parametros que rol1, se crea, pero este apunta
    # al proyectoPrueba2)
    assert str([data[0], data[1], data[2], data[3]]) == str(["Rol Interno 1", "Interno", "Descripcion 1",
                                                             proyectoPrueba2.id]), \
        "Error en controller de importar roles internos de proyecto"

    # Verificamos el status del response
    assert response.status_code == 201, "Error al verificar status de controller de importar rol"
