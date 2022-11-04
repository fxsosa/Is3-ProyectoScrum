import pytest
import pytz

from historiasDeUsuario.models import Tipo_Historia_Usuario
from historiasDeUsuario_proyecto.models import historiaUsuario
from proyectos.models import Proyecto, participante
from sprints.models import Sprint, Sprint_Miembro_Equipo, SprintBacklog
from usuarios.models import Usuario
from django.contrib.auth import get_user_model
import datetime

@pytest.mark.django_db
def test_crearSprint():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)

    assert str([sprint.nombre, sprint.descripcion, sprint.cantidadDias, sprint.capacidadEquipo,
                sprint.proyecto_id]) == str(["Sprint 1", "Descripcion de Sprint", 30, 30, proyecto.id]), "Error al crear sprint"


@pytest.mark.django_db
def test_CrearSprintBacklog():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)
    # Agregamos otro usuario
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    idProyecto = proyecto.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})

    Sprint_Miembro_Equipo.objects.agregarMiembro({"capacidad": 50, "sprint_id": sprint.id,
                                                  "usuario_id": user1.id})

    idParticipante = part.id
    datos = {
        "nombre": "Historia 1",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    datos = {
        "nombre": "Historia 2",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia2 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    Proyecto.objects.iniciarProyecto({"id": proyecto.id})

    sprintBacklog = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprint.id, opcion="Avanzar")
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia1[0].id)
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia2[0].id)
    listaHUBacklog = SprintBacklog.objects.listarHistoriasUsuario(proyecto_id=proyecto.id, sprint_id=sprint.id)
    historia1 = historiaUsuario.objects.filter(id=historia1[0].id)
    historia2 = historiaUsuario.objects.filter(id=historia2[0].id)

    assert str([listaHUBacklog[0].id, listaHUBacklog[1].id]) == str([historia1[0].id, historia2[0].id]), "Error al crear el sprint backlog"


@pytest.mark.django_db
def test_ListarTiposHUSprintBacklog():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)
    # Agregamos otro usuario
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    idProyecto = proyecto.id
    tipo1 = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    tipo2 = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                       "id_proyecto": idProyecto,
                                                       "columnas": ["Columna 1", "Columna 2", "Columna 3"]})
    idTipo1 = tipo1.id
    idTipo2 = tipo2.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})

    Sprint_Miembro_Equipo.objects.agregarMiembro({"capacidad": 50, "sprint_id": sprint.id,
                                                  "usuario_id": user1.id})

    idParticipante = part.id
    datos = {
        "nombre": "Historia 1",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo1,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    datos = {
        "nombre": "Historia 2",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo2,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia2 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    Proyecto.objects.iniciarProyecto({"id": proyecto.id})

    sprintBacklog = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprint.id, opcion="Avanzar")
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia1[0].id)
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia2[0].id)
    listaTiposHU = SprintBacklog.objects.listarTipoHUSprint(idProyecto=proyecto.id, idSprint=sprint.id)

    # Verificamos que los ID recibidos de la lista de Tipos, coincidan con los ID de los tipos que cargamos
    # en las historias del sprint
    assert str([listaTiposHU[0].id, listaTiposHU[1].id]) == str([tipo1.id, tipo2.id]), "Error al listar Tipos de HU de un Sprint"


@pytest.mark.django_db
def test_ListarHUTipo():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)
    # Agregamos otro usuario
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    idProyecto = proyecto.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})

    Sprint_Miembro_Equipo.objects.agregarMiembro({"capacidad": 50, "sprint_id": sprint.id,
                                                  "usuario_id": user1.id})

    idParticipante = part.id
    datos = {
        "nombre": "Historia 1",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    datos = {
        "nombre": "Historia 2",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia2 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    Proyecto.objects.iniciarProyecto({"id": proyecto.id})

    sprintBacklog = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprint.id, opcion="Avanzar")
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia1[0].id)
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia2[0].id)
    listaHU = SprintBacklog.objects.listarHUTipo(proyecto_id=proyecto.id, sprint_id=sprint.id, tipo_id=tipo.id)

    # Verificamos que los US del sprint backlog obtenidos, sean del mismo tipo que el tipo creado
    assert str([listaHU[0].tipo_historia_usuario.id, listaHU[1].tipo_historia_usuario.id]) == str([tipo.id, tipo.id]), \
        "Error al listar los US de un Tipo, de un Sprint"


@pytest.mark.django_db
def test_EliminarHUSprintBacklog():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)

    idProyecto = proyecto.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})

    Sprint_Miembro_Equipo.objects.agregarMiembro({"capacidad": 50, "sprint_id": sprint.id,
                                                  "usuario_id": user1.id})

    idParticipante = part.id
    datos = {
        "nombre": "Historia 1",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    Proyecto.objects.iniciarProyecto({"id": proyecto.id})

    sprintBacklog = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprint.id, opcion="Avanzar")
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia[0].id)

    # Verificamos que el metodo nos confirme la eliminacion (Boolean)
    assert SprintBacklog.objects.eliminarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprint.id, idHistoria=historia[0].id) == True, "Error al eliminar HU del Sprint Backlog"


@pytest.mark.django_db
def test_AgregarMiembroSprint():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)

    datos = {
        "capacidad": 5,
        "sprint_id": sprint.id,
        "usuario_id": user1.id
    }
    equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    assert str(equipo.__str__()) == str([equipo.usuario.id, equipo.sprint.id, str(equipo.capacidad)]), "Error al crear miembro de un Sprint"

@pytest.mark.django_db
def test_ModificarMiembroSprint():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)

    # Los datos originales de este miembro de sprint
    datos = {
        "capacidad": 5,
        "sprint_id": sprint.id,
        "usuario_id": user1.id
    }
    equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    # Modificamos las capacidad de 5 a 10 para este miembro del sprint
    equipoActualizado = Sprint_Miembro_Equipo.objects.modificarMiembro({"miembro_equipo_id": equipo.id,
                                                                        "capacidad": 8,
                                                                        "sprint_id": sprint.id})

    assert str(equipoActualizado.__str__()) == str([equipo.usuario.id, equipo.sprint.id, '8']), "Error al modificar miembro de un Sprint"

@pytest.mark.django_db
def test_EliminarMiembroSprint():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint = Sprint.objects.crearSprint(datos=datosSprint)
    sprint = Sprint.objects.get(id=sprint[0].id)

    # Los datos originales de este miembro de sprint
    datos = {
        "capacidad": 5,
        "sprint_id": sprint.id,
        "usuario_id": user1.id
    }
    miembro_equipo = Sprint_Miembro_Equipo.objects.agregarMiembro(datos=datos)

    assert Sprint_Miembro_Equipo.objects.eliminarMiembro(idSprint=sprint.id,
                                                         idProyecto=proyecto.id,
                                                         id_miembro_equipo=miembro_equipo.id) == True, \
        "Error al eliminar miembro de un Sprint"



@pytest.mark.django_db
def test_obtenerSprint():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprintCreado = Sprint.objects.crearSprint(datos=datosSprint)
    sprintObtenido = Sprint.objects.obtenerSprint(idProyecto=proyecto.id, idSprint=sprintCreado[0].id)

    assert str([sprintObtenido[0].id, sprintObtenido[0].fecha_inicio, sprintObtenido[0].fecha_fin,
                sprintObtenido[0].cantidadDias, sprintObtenido[0].estado,
                sprintObtenido[0].capacidadEquipo, sprintObtenido[0].proyecto_id]) == str([sprintCreado[0].id,
                None, None, 30, 'Creado', 30, proyecto.id])

@pytest.mark.django_db
def test_eliminarSprint():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprintCreado = Sprint.objects.crearSprint(datos=datosSprint)
    # Esta funcion cambia el estado del sprint a "Cancelado"
    assert True is Sprint.objects.eliminarSprint(idProyecto=proyecto.id, idSprint=sprintCreado[0].id)
    sprintCancelado = Sprint.objects.obtenerSprint(idProyecto=proyecto.id, idSprint=sprintCreado[0].id)
    # Verificamos que el estado del Sprint haya cambiado a "Cancelado"
    assert str([sprintCancelado[0].id, sprintCancelado[0].fecha_inicio, sprintCancelado[0].fecha_fin,
                sprintCancelado[0].cantidadDias, sprintCancelado[0].estado,
                sprintCancelado[0].capacidadEquipo, sprintCancelado[0].proyecto_id]) == str([sprintCreado[0].id,
                None, None, 30, 'Cancelado', 30, proyecto.id]), "Error al cancelar un Sprint"

@pytest.mark.django_db
def test_cambiarEstadoSprint():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprintCreado = Sprint.objects.crearSprint(datos=datosSprint)

    idProyecto = proyecto.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    Sprint_Miembro_Equipo.objects.agregarMiembro({"capacidad": 50, "sprint_id": sprintCreado[0].id,
                                                  "usuario_id": user1.id})
    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    datos = {
        "nombre": "Historia 1",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)
    datos = {
        "nombre": "Historia 2",
        "descripcion": "Descripcion de Prueba",
        "prioridad_tecnica": 1,
        "prioridad_negocio": 2,
        "estimacion_horas": 10,
        "idTipo": idTipo,
        "idParticipante": idParticipante,
        "idProyecto": idProyecto,
    }
    historia2 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos, user=user1)

    # Actualizamos el estado del proyecto
    Proyecto.objects.iniciarProyecto({"id": idProyecto})

    sprintActualizado = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprintCreado[0].id,
                                                     opcion="Avanzar")
    sprintActualizado = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprintCreado[0].id,
                                                     opcion="Avanzar")
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprintCreado[0].id, idHistoria=historia1[0].id)
    SprintBacklog.objects.agregarHUSprintBacklog(idProyecto=proyecto.id, idSprint=sprintCreado[0].id, idHistoria=historia2[0].id)

    # Verificamos que el estado del Sprint haya cambiado a "En Ejecucion"
    assert str([sprintActualizado[0].id, sprintActualizado[0].fecha_inicio, sprintActualizado[0].fecha_fin,
                sprintActualizado[0].cantidadDias, sprintActualizado[0].estado,
                sprintActualizado[0].proyecto_id]) == str([sprintCreado[0].id,
                                                        sprintCreado[0].fecha_inicio,
                                                        sprintCreado[0].fecha_fin, 30,
                                                        'En Ejecución',
                                                        proyecto.id]), "Error al pasar de estado Planificacion a En Ejecucion"

    # Verificamos que el estado del Sprint haya cambiado a "Finalizado"
    sprintActualizado = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprintCreado[0].id,
                                                     opcion="Avanzar")
    # Verificamos que el estado del Sprint haya cambiado a "En Ejecucion"
    assert str([sprintActualizado[0].id, sprintActualizado[0].fecha_inicio, sprintActualizado[0].fecha_fin,
                sprintActualizado[0].cantidadDias, sprintActualizado[0].estado,
                sprintActualizado[0].proyecto_id]) == str([sprintCreado[0].id,
                                                         sprintCreado[0].fecha_inicio,
                                                         sprintCreado[0].fecha_fin, 30,
                                                        'Finalizado',
                                                        proyecto.id]), "Error al pasar de estado En Ejecucion a Finalizado"

@pytest.mark.django_db
def test_listarSprints():
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
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 1",
        "cantidadDias": 30,
        "capacidadEquipo": 30
    }
    sprint1Creado = Sprint.objects.crearSprint(datos=datosSprint)
    Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprint1Creado[0].id, opcion="Avanzar")
    datosSprint = {
        "idProyecto": proyecto.id,
        "descripcion": "Descripcion de Sprint",
        "nombre": "Sprint 2",
        "cantidadDias": 30,
        "capacidadEquipo": 60
    }
    sprint2Creado = Sprint.objects.crearSprint(datos=datosSprint)

    # Listamos los sprints del proyecto (probamos con 2 Sprints de proyectos, sprint1Creado y sprint2Creado)
    listaSprints = Sprint.objects.listarSprints(idProyecto=proyecto.id)

    assert str([listaSprints[0].id, listaSprints[0].nombre, listaSprints[0].descripcion,
                listaSprints[0].cantidadDias, listaSprints[0].capacidadEquipo, listaSprints[0].estado,
                listaSprints[1].id, listaSprints[1].nombre, listaSprints[1].descripcion,
                listaSprints[1].cantidadDias, listaSprints[1].capacidadEquipo, listaSprints[1].estado]) == str([
        sprint2Creado[0].id, "Sprint 2", "Descripcion de Sprint", 30, 60, "Creado",
        sprint1Creado[0].id, "Sprint 1", "Descripcion de Sprint", 30, 30, "Planificación"]), "Error al listar los " \
                                                                                             "sprints de un proyecto"
