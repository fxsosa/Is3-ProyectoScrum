import datetime
import json
import ast
import pytest
import pytz
from django.contrib.auth import get_user_model
from rest_framework import request
import jwt
from django.test import Client
from django.core import serializers

from historiasDeUsuario.models import Tipo_Historia_Usuario
from historiasDeUsuario_proyecto.models import historiaUsuario
from proyectos.models import Proyecto, participante
from roles.models import Rol
from sprints.models import Sprint, Sprint_Miembro_Equipo

tokenAnonymous = "Bearer " + jwt.encode(key="secret", payload={"email": "AnonymousUser",
                   "password": None,
                   "given_name": "",
                   "family_name": "",
                   "rol": None})


@pytest.mark.django_db
def test_controllerSprint_post():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.crear_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/sprints/', content_type='application/json',
                      data={"idProyecto": proyecto.id, "nombre": "Sprint 1", "descripcion": "Sprint de Prueba",
                            "capacidadEquipo": 50, "cantidadDias": 32})

    data = json.loads(response.content)[0]
    print(data)
    data=data['fields']

    # Verificamos el status del response
    assert response.status_code == 201, "Error al verificar el estatus del response del controller de crear sprint"

    # Verificamos los datos del response
    assert str([data['nombre'], data['descripcion'],  data['cantidadDias']]) == str([
        "Sprint 1", "Sprint de Prueba", 32]), "Error al verificar response del controller de crear sprint"


@pytest.mark.django_db
def test_controllerSprint_get():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.obtener_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/sprints/?idProyecto=' + str(proyecto.id) + '&idSprint=' + str(sprint[0].id))

    data = json.loads(response.content)[0]
    print(data)

    # Verificando el status del response
    assert response.status_code == 200, "Error al verificar el status del response del controller de obtener sprint"

    # Verificando data del response
    assert str([data['fields']['nombre'], data['fields']['descripcion'], data['fields']['cantidadDias']]) == str([
        "Sprint 1", "Sprint de Prueba", 32]), "Error en los datos del controller de obtener sprint"


@pytest.mark.django_db
def test_controllerSprint_put():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)
    sprint.estado="Planificación"
    sprint.save()
    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.actualizar_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/sprints/', content_type='application/json',
                     data={"idProyecto": proyecto.id,
                           "idSprint": sprint.id,
                           "nombre": "Nombre Actualizado",
                           "descripcion": "Descripcion Actualizada",
                           "cantidadDias": 20})

    data = json.loads(response.content)[0]
    print(data)

    # Verificamos el status del response
    assert response.status_code == 201#, "Error al verificar el estatus del controller de actualizar sprint"

    # Verificamos data del response
    assert str([data['fields']['nombre'], data['fields']['descripcion'], data['fields']['cantidadDias']]) == str([
        "Nombre Actualizado", "Descripcion Actualizada", 20]), "Error al verificar datos del response del controller de actualizar sprint"


@pytest.mark.django_db
def test_controllerSprint_delete():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.borrar_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.delete('/api/v1/sprints/?idProyecto=' + str(proyecto.id) + '&idSprint=' + str(sprint[0].id))

    data = response.content.decode("utf-8")

    # Verificamos el status del response
    assert response.status_code == 201, "Error al verificar el estatus del response del controller de eliminar sprint"

    # Verificamos los datos del response
    assert data == "Sprint eliminado con exito!", "Error al verificar los datos del response del controller de eliminar sprint"


@pytest.mark.django_db
def test_controllerListarSprints_get():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba 1",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    datosSprint = {
        "nombre": "Sprint 2",
        "descripcion": "Sprint de Prueba 2",
        "idProyecto": proyecto.id,
        "cantidadDias": 33,
        "capacidadEquipo": 50
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.listar_sprint_proyecto", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/sprints/listar?idProyecto=' + str(proyecto.id))

    data = json.loads(response.content)

    # Verificando el status del response
    assert response.status_code == 200, "Error al verificar el estatus del controller de listar sprints de proyecto"

    # Verificando datos del response
    assert str([data[0]['fields']['nombre'], data[0]['fields']['descripcion'], data[0]['fields']['cantidadDias'],
                data[1]['fields']['nombre'], data[1]['fields']['descripcion'], data[1]['fields']['cantidadDias']]) == str([
        "Sprint 2", "Sprint de Prueba 2", 33,
        "Sprint 1", "Sprint de Prueba 1", 32]), "Error al verificar los datos del controller de listar sprints de proyecto"

@pytest.mark.django_db
def test_controllerEquipoSprint_post():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint = {
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno",
                                      idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.agregar_miembro_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/sprints/equipo', content_type='application/json',
                      data={"proyecto_id": proyecto.id,
                            "usuario_id": user1.id,
                            "sprint_id": sprint[0].id,
                            "capacidad": 10})


    # Verificamos el status del response
    assert response.status_code == 201, "Error al verificar el estatus del response del controller de agregar miembro de equipo de sprint"

@pytest.mark.django_db
def test_controllerEquipoSprint_get():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    datosMiembro = {"proyecto_id": proyecto.id,
            "usuario_id": user1.id,
            "sprint_id": sprint[0].id,
            "capacidad": 10}

    miembro_equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datosMiembro)


    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.ver_equipo_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/sprints/equipo?idProyecto=' + str(proyecto.id) + '&idSprint=' + str(sprint[0].id))

    # Verificando el status del response
    assert response.status_code == 200, "Error en controller de obtener miembro de equipo de un sprint"


@pytest.mark.django_db
def test_controllerEquipoSprint_put():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    datosMiembro = {"proyecto_id": proyecto.id,
            "usuario_id": user1.id,
            "sprint_id": sprint[0].id,
            "capacidad": 10}

    miembro_equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datosMiembro)


    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.modificar_miembro_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/sprints/equipo', content_type='application/json',
                   data={"proyecto_id": proyecto.id,
                         "sprint_id": sprint[0].id,
                         "miembro_equipo_id": miembro_equipo.id,
                         "capacidad": 20})

    data = response.content.decode("utf-8")
    print(data)
    # Verificando el status del response
    assert response.status_code == 201, "Error en controller de actualizar miembro de equipo de un sprint"


@pytest.mark.django_db
def test_controllerEquipoSprint_delete():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    datosSprint={
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    datosMiembro = {"proyecto_id": proyecto.id,
            "usuario_id": user1.id,
            "sprint_id": sprint[0].id,
            "capacidad": 10}

    miembro_equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datosMiembro)


    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno", idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.borrar_miembro_sprint", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.delete('/api/v1/sprints/equipo?idProyecto=' + str(proyecto.id) + '&idSprint=' + str(sprint[0].id) + '&idMiembroEquipo=' + str(miembro_equipo.id))

    data = response.content.decode("utf-8")

    # Verificamos el status del response
    assert response.status_code == 201, "Error al verificar el estatus del response del controller de eliminar miembro de sprint"

    # Verificamos los datos del response
    assert data == "Miembro del equipo eliminado con exito!", "Error al verificar los datos del response del controller de eliminar miembro de sprint"


@pytest.mark.django_db
def test_controllerReasignarDesarrollador_put():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )
    user2 = User.objects.create_user(email='user@email2.com', password='abcdefg', username='username1',
                                     nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', )

    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    datosProyecto = {
        "nombre": "Proyecto Prueba",
        "descripcion": "Proyecto de Prueba",
        "fechaInicio": auxDateTime1,
        "fechaFin": auxDateTime2,
        "scrumMaster": "user@email.com",
        "estado": "En Espera"
    }
    proyecto = Proyecto.objects.crearProyecto(datos=datosProyecto)
    participante1 = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id,
                                                  "idUsuario": user1.id})
    participante2 = participante.objects.crearParticipante(datos={"idProyecto": proyecto.id,
                                                  "idUsuario": user2.id})
    datosSprint = {
        "nombre": "Sprint 1",
        "descripcion": "Sprint de Prueba",
        "idProyecto": proyecto.id,
        "cantidadDias": 32,
        "capacidadEquipo": 50,
        "estado": "Planificación"
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    datosMiembro = {"proyecto_id": proyecto.id,
                    "usuario_id": user1.id,
                    "sprint_id": sprint[0].id,
                    "capacidad": 10}

    miembro_equipo1 = Sprint_Miembro_Equipo.objects.agregarMiembro(datosMiembro)
    datosMiembro = {"proyecto_id": proyecto.id,
                    "usuario_id": user2.id,
                    "sprint_id": sprint[0].id,
                    "capacidad": 10}
    miembro_equipo1 = Sprint_Miembro_Equipo.objects.agregarMiembro(datosMiembro)

    # Cambiamos el estado del sprint a "En Ejecución"
    sprint = Sprint.objects.get(id=sprint[0].id)
    sprint.estado = "En Ejecución"
    sprint.save()

    # Creamos las US y asignamos al nuevo miembro de sprint participante
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": proyecto.id,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    datos = {
        "nombre": "Historia 1",
        "descripcion": "Descripcion 1",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": tipo.id,
        "idParticipante": participante1.id,
        "idProyecto": proyecto.id
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    datos = {
        "nombre": "Historia 2",
        "descripcion": "Descripcion 2",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": tipo.id,
        "idParticipante": participante1.id,
        "idProyecto": proyecto.id
    }
    historia2 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolInterno(nombre="Rol Interno", descripcion="Descripcion de Rol Interno",
                                      idProyecto=proyecto.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.reasignar_historias", objeto=proyecto)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/sprints/reasignar-historias', content_type='application/json',
                     data={"idProyecto": proyecto.id,
                           "idSprint": sprint.id,
                           "idUsuario1": user1.id,
                           "idUsuario2": user2.id})

    data = response.content.decode("utf-8")
    print(data)

    # Verificando el status del response
    assert response.status_code == 200#, "Error en controller de reasignar historias de usuario"

    # Verificando el data del response
    assert data == "Reasignacion de historias de usuario realizada con exito!", "Error al verificar los datos del controller de reasignar historias de usuario"