import json
import ast
import pytest
from django.contrib.auth import get_user_model
from rest_framework import request
import jwt
from django.test import Client
from django.core import serializers

from historiasDeUsuario.models import Columna_Tipo_Historia_Usuario, Tipo_Historia_Usuario
from historiasDeUsuario_proyecto.models import ActividadesUS, historiaUsuario
from proyectos.models import Proyecto, participante
from roles.models import Rol
from sprints.models import SprintBacklog, Sprint_Miembro_Equipo, Sprint
from usuarios.models import Usuario

tokenAnonymous = "Bearer " + jwt.encode(key="secret", payload={"email": "AnonymousUser",
                   "password": None,
                   "given_name": "",
                   "family_name": "",
                   "rol": None})


@pytest.mark.django_db
def test_controllerListarHistorialUS_get():
    User = get_user_model()
    userAnonimo = User.objects.get(email="AnonymousUser")
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=userAnonimo, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre Original",
        "descripcion": "Descripcion Original",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    # Extraemos las columnas del tablero kanban
    listaColumnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=idTipo)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia[0].id,
                                                                     "idParticipante": user1.id,
                                                                     "idTipo": idTipo,
                                                                     "nombre": "Nombre Actualizado",
                                                                     "descripcion": "Descripcion Actualizada",
                                                                     "prioridad_tecnica": None,
                                                                     "horas_trabajadas": 0,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": listaColumnas[0].id}, False, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.obtener_historia_usuario",
                                       objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/historiasUsuario/historial/listar?idProyecto=' + str(proyectoPrueba.id) + '&idHistoria=' + str(historia[0].id))

    print("Response es: ")
    print(response)
    data = json.loads(response.content)
    print("Data es:")
    print(data)

    # Verificando los datos del response
    # Verificamos los history_change_reason sean: Creado  - Actualizado (porque esas fueran las operaciones que realizamos)
    # Tambien verificamos que el nombre y descripcion coincidan con cada version
    assert str([data[1]['fields']['nombre'], data[1]['fields']['descripcion'], data[1]['fields']['history_change_reason'],
                data[0]['fields']['nombre'], data[0]['fields']['descripcion'], data[0]['fields']['history_change_reason']]) == str([
        "Nombre Original", "Descripcion Original", "Creado",
        "Nombre Actualizado", "Descripcion Actualizada", "Actualizado"]), "Error en controller de obtener historial de US"


    # Verificamos el status del response
    assert response.status_code == 200, "Error en verificar status del controller de listar historial de US"



@pytest.mark.django_db
def test_controllerHistorialUS_get():
    User = get_user_model()
    userAnonimo = User.objects.get(email="AnonymousUser")
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=userAnonimo, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre Original",
        "descripcion": "Descripcion Original",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.obtener_historia_usuario",
                                       objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Obtenemos la version creada (para extraer el id a enviar en el request)
    version = historia[0].history.filter(history_change_reason="Creado")
    idVersion = version[0].history_id

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/historiasUsuario/historial?idProyecto=' + str(proyectoPrueba.id) + '&idHistoria=' +
                     str(historia[0].id) + '&idVersion=' + str(idVersion))

    print("Response.content es: ")
    print(response.content)
    # Convertimos a string
    data = response.content.decode("utf-8")
    # Eliminamos el segundo array (no necesitamos verificar el array de diferencias)
    data = data[0:len(data) - 2]
    # Convertimos a bytes
    data = str.encode(data)

    # Convertimos a diccionario
    data = json.loads(data)

    # Verificamos los datos del response
    # Tiene que ser la version "Creado"
    assert str([data[0]['fields']['nombre'],
                data[0]['fields']['descripcion'],
                data[0]['fields']['history_change_reason']]) == str(["Nombre Original",
                                                                     "Descripcion Original",
                                                                     "Creado"])\
        , "Error en controller de obtener una version del historial de US"


    # Verificamos el status del response
    assert response.status_code == 200, "Error al verificar status del controller de obtener una version del historial"



@pytest.mark.django_db
def test_controllerHistorialUS_put():
    User = get_user_model()
    userAnonimo = User.objects.get(email="AnonymousUser")
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=userAnonimo, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre Original",
        "descripcion": "Descripcion Original",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    # Extraemos las columnas del tablero kanban
    listaColumnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=idTipo)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia[0].id,
                                                                     "idParticipante": user1.id,
                                                                     "idTipo": idTipo,
                                                                     "nombre": "Nombre Actualizado",
                                                                     "descripcion": "Descripcion Actualizada",
                                                                     "prioridad_tecnica": None,
                                                                     "horas_trabajadas": 0,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": listaColumnas[0].id}, False, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.restaurar_historia_usuario",
                                       objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Obtenemos la version anterior
    primeraVersion = historia[0].history.earliest()
    print("La primera version es: ")
    print(primeraVersion)
    idVersion = primeraVersion.history_id

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.put('/api/v1/historiasUsuario/historial',
                     content_type='application/json',
                     data={"idProyecto": proyectoPrueba.id,
                           "idHistoria": historia[0].id,
                           "idVersion": idVersion})

    data = json.loads(response.content)

    # Verificando los datos del response
    # Verificamos los datos sean de la version original (el creado, no el actualizado)
    assert str([data[0]['fields']['nombre'],
                data[0]['fields']['descripcion']]) == str(["Nombre Original",
                                                           "Descripcion Original"])\
        , "Error en controller de restaurar historial de US"


    # Verificamos el status del response
    assert response.status_code == 201, "Error en verificar status del controller de listar historial de US"



@pytest.mark.django_db
def test_controllerActividadesUS_get():
    User = get_user_model()
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre de Prueba",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    # Extraemos las columnas del tablero kanban
    listaColumnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=idTipo)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia[0].id,
                                                                     "idParticipante": user1.id,
                                                                     "idTipo": idTipo, "nombre": None,
                                                                     "descripcion": None,
                                                                     "prioridad_tecnica": None,
                                                                     "horas_trabajadas": 0,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": listaColumnas[0].id}, False, user=user1)

    # Creamos un sprint
    sprintCreado = Sprint.objects.crearSprint(datos={"nombre": "Sprint Prueba",
                                                     "descripcion": "Descripcion",
                                                     "idProyecto": idProyecto,
                                                     "cantidadDias": 40,
                                                     "capacidadEquipo": 30})

    # Pasamos el proyecto al estado en iniciado
    Proyecto.objects.iniciarProyecto(datos={"id": proyectoPrueba.id})
    # Creamos un miembro de equipo y agregamos al sprint
    # Los datos originales de este miembro de sprint
    datos = {
        "capacidad": 5,
        "sprint_id": sprintCreado[0].id,
        "usuario_id": user1.id
    }
    equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    # Pasamos al estado Planificacion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")
    # Pasamos al estado En Ejecucion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")

    # Agregamos el US al sprint
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=idProyecto, idSprint=sprintCreado[0].id,
                                                 idHistoria=historia[0].id)

    # Creamos la actividad
    actividad = ActividadesUS.objects.crearActividad(datos={"titulo": "Actividad 1",
                                                            "descripcion": "Descripcion Actividad",
                                                            "horasTrabajadas": 1,
                                                            "idHistoria": historia[0].id,
                                                            "idProyecto": idProyecto,
                                                            "idSprint": sprintCreado[0].id}, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.obtener_actividad_historia_usuario", objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/historiasUsuario/actividad?idProyecto=' + str(idProyecto) + '&idHistoria=' +
                     str(historia[0].id) + '&idActividad=' + str(actividad[0].id))

    data = json.loads(response.content)[0]

    # Verificamos los datos del response
    assert str([data['pk'], data['fields']['titulo'], data['fields']['descripcion']]) == str([
        actividad[0].id, "Actividad 1", "Descripcion Actividad"]), "Error en controller de obtener actividad de US"

    # Verificamos el status del response
    assert response.status_code == 200, "Error al verificar el status del responde del controller de obtener actividad"


@pytest.mark.django_db
def test_controllerActividadesUS_post():
    User = get_user_model()
    # Obtenemos el usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")

    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    # Agregamos al usuario anonimo al proyecto
    participante_anonimo=participante.objects.crearParticipante({"idUsuario": userAnonimo.id, "idProyecto": idProyecto})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre de Prueba",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": participante_anonimo.id,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    # Extraemos las columnas del tablero kanban
    listaColumnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=idTipo)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia[0].id,
                                                                     "idParticipante": userAnonimo.id,
                                                                     "idTipo": idTipo, "nombre": None,
                                                                     "descripcion": None,
                                                                     "prioridad_tecnica": None,
                                                                     "horas_trabajadas": 0,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": listaColumnas[0].id}, False, user=user1)

    # Creamos un sprint
    sprintCreado = Sprint.objects.crearSprint(datos={"nombre": "Sprint Prueba",
                                                     "descripcion": "Descripcion",
                                                     "idProyecto": idProyecto,
                                                     "cantidadDias": 40,
                                                     "capacidadEquipo": 30})

    # Pasamos el proyecto al estado en iniciado
    Proyecto.objects.iniciarProyecto(datos={"id": proyectoPrueba.id})
    # Creamos un miembro de equipo y agregamos al sprint
    # Los datos originales de este miembro de sprint
    datos = {
        "capacidad": 5,
        "sprint_id": sprintCreado[0].id,
        "usuario_id": userAnonimo.id
    }
    equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    # Pasamos al estado Planificacion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")
    # Pasamos al estado En Ejecucion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")

    # Agregamos el US al sprint
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=idProyecto, idSprint=sprintCreado[0].id,
                                                 idHistoria=historia[0].id)




    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.crear_actividad_historia_usuario",
                                       objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.post('/api/v1/historiasUsuario/actividad', content_type='application/json',
                      data={"titulo": "Actividad 1",
                             "descripcion": "Descripcion Actividad",
                             "horasTrabajadas": 1,
                             "idHistoria": historia[0].id,
                             "idProyecto": idProyecto,
                             "idSprint": sprintCreado[0].id})

    data = json.loads(response.content)[0]
    print("Data es:")
    print(data)

    # Verificamos datos del response
    assert str([data['fields']['titulo'], data['fields']['descripcion'], data['fields']['horasTrabajadas']]) == str([
        "Actividad 1", "Descripcion Actividad", 1]), "Error en controller de crear actividad de US"

    # Verificamos el status del response
    assert response.status_code == 201, "Error en obtener el status del controller de crear actividad"


@pytest.mark.django_db
def test_controllerActividadesUS_delete():
    User = get_user_model()
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre de Prueba",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    # Extraemos las columnas del tablero kanban
    listaColumnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=idTipo)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia[0].id,
                                                                     "idParticipante": user1.id,
                                                                     "idTipo": idTipo, "nombre": None,
                                                                     "descripcion": None,
                                                                     "prioridad_tecnica": None,
                                                                     "horas_trabajadas": 0,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": listaColumnas[0].id}, False, user=user1)

    # Creamos un sprint
    sprintCreado = Sprint.objects.crearSprint(datos={"nombre": "Sprint Prueba",
                                                     "descripcion": "Descripcion",
                                                     "idProyecto": idProyecto,
                                                     "cantidadDias": 40,
                                                     "capacidadEquipo": 30})

    # Pasamos el proyecto al estado en iniciado
    Proyecto.objects.iniciarProyecto(datos={"id": proyectoPrueba.id})
    # Creamos un miembro de equipo y agregamos al sprint
    # Los datos originales de este miembro de sprint
    datos = {
        "capacidad": 5,
        "sprint_id": sprintCreado[0].id,
        "usuario_id": user1.id
    }
    equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    # Pasamos al estado Planificacion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")
    # Pasamos al estado En Ejecucion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")

    # Agregamos el US al sprint
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=idProyecto, idSprint=sprintCreado[0].id,
                                                 idHistoria=historia[0].id)

    # Creamos la actividad
    actividad = ActividadesUS.objects.crearActividad(datos={"titulo": "Actividad 1",
                                                            "descripcion": "Descripcion Actividad",
                                                            "horasTrabajadas": 1,
                                                            "idHistoria": historia[0].id,
                                                            "idProyecto": idProyecto,
                                                            "idSprint": sprintCreado[0].id}, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.eliminar_actividad_historia_usuario",
                                       objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.delete('/api/v1/historiasUsuario/actividad?idProyecto=' + str(proyectoPrueba.id) +
                        '&idHistoria='+ str(historia[0].id) +'&idActividad=' + str(actividad[0].id))

    data = response.content.decode("utf-8")

    # Verificamos datos del response
    assert data == "Eliminado con exito!", "Error en controller de eliminar actividad de US"

    # Verificamos el status del response
    assert response.status_code == 200, "Error al verificar el status del controller de eliminar actividad de US"


@pytest.mark.django_db
def test_controllerListarActividadesUS_get():
    User = get_user_model()
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3", ]})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Nombre de Prueba",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    # Extraemos las columnas del tablero kanban
    listaColumnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id_HU=idTipo)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia[0].id,
                                                                     "idParticipante": user1.id,
                                                                     "idTipo": idTipo, "nombre": None,
                                                                     "descripcion": None,
                                                                     "prioridad_tecnica": None,
                                                                     "horas_trabajadas": 0,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": listaColumnas[0].id}, False, user=user1)

    # Creamos un sprint
    sprintCreado = Sprint.objects.crearSprint(datos={"nombre": "Sprint Prueba",
                                                     "descripcion": "Descripcion",
                                                     "idProyecto": idProyecto,
                                                     "cantidadDias": 40,
                                                     "capacidadEquipo": 30})

    # Pasamos el proyecto al estado en iniciado
    Proyecto.objects.iniciarProyecto(datos={"id": proyectoPrueba.id})
    # Creamos un miembro de equipo y agregamos al sprint
    # Los datos originales de este miembro de sprint
    datos = {
        "capacidad": 5,
        "sprint_id": sprintCreado[0].id,
        "usuario_id": user1.id
    }
    equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    # Pasamos al estado Planificacion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")
    # Pasamos al estado En Ejecucion
    Sprint.objects.cambiarEstado(idProyecto=idProyecto, idSprint=sprintCreado[0].id, opcion="Avanzar")

    # Agregamos el US al sprint
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=idProyecto, idSprint=sprintCreado[0].id,
                                                 idHistoria=historia[0].id)

    # Creamos la actividad 1
    actividad1 = ActividadesUS.objects.crearActividad(datos={"titulo": "Actividad 1",
                                                            "descripcion": "Descripcion Actividad 1",
                                                            "horasTrabajadas": 1,
                                                            "idHistoria": historia[0].id,
                                                            "idProyecto": idProyecto,
                                                            "idSprint": sprintCreado[0].id}, user=user1)

    # Creamos la actividad 2
    actividad2 = ActividadesUS.objects.crearActividad(datos={"titulo": "Actividad 2",
                                                            "descripcion": "Descripcion Actividad 2",
                                                            "horasTrabajadas": 1,
                                                            "idHistoria": historia[0].id,
                                                            "idProyecto": idProyecto,
                                                            "idSprint": sprintCreado[0].id}, user=user1)

    # Creamos el rol y asignamos al usuario anonimo
    userAnonimo = User.objects.get(email="AnonymousUser")
    rol = Rol.objects.crearRolExterno(nombre="Rol Externo", descripcion="Descripcion de Rol Externo")
    Rol.objects.agregarPermisoDeObjeto(idRol=rol.id, nombrePermiso="proyectos.listar_actividad_historia_usuario",
                                       objeto=proyectoPrueba)
    Rol.objects.asignarRolaUsuario(idRol=rol.id, user=userAnonimo)

    # Realizamos el request
    c = Client(HTTP_AUTHORIZATION=tokenAnonymous)
    response = c.get('/api/v1/historiasUsuario/actividad/listar?idProyecto=' + str(proyectoPrueba.id) +
                     '&idHistoria=' + str(historia[0].id))

    data = json.loads(response.content)

    print("Data es:")
    print(data)

    # Verificamos los datos del response
    assert str([data[0]['pk'], data[0]['fields']['titulo'], data[0]['fields']['descripcion'], data[0]['fields']['horasTrabajadas'],
                data[1]['pk'], data[1]['fields']['titulo'], data[1]['fields']['descripcion'], data[1]['fields']['horasTrabajadas']]) == str([
        actividad1[0].id, "Actividad 1", "Descripcion Actividad 1", 1,
        actividad2[0].id, "Actividad 2", "Descripcion Actividad 2", 1]), "Error en controller de listar actividades de US"

    # Verificamos el status del response
    assert response.status_code == 200, "Error al verificar el status del controller de listar actividades de US"