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
                sprint.proyecto_id]) == str(["Sprint 1", "Descripcion de Sprint", 30, 30, proyecto.id])


@pytest.mark.django_db
def test_SprintBacklog():
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
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos)
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
    historia2 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos)

    sprintBacklog = Sprint.objects.cambiarEstado(idProyecto=proyecto.id, idSprint=sprint.id, opcion="Avanzar")
    listaHUBacklog = SprintBacklog.objects.listarHistoriasUsuario(proyecto_id=proyecto.id, sprint_id=sprint.id)
    historia1 = historiaUsuario.objects.filter(id=historia1[0].id)
    historia2 = historiaUsuario.objects.filter(id=historia2[0].id)

    assert str([listaHUBacklog[0].id, listaHUBacklog[1].id]) == str([historia1[0].id, historia2[0].id])


@pytest.mark.django_db
def test_SprintEquipo():
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

    assert str(equipo.__str__()) == str([equipo.usuario.id, equipo.sprint.id, str(equipo.capacidad)])

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
                None, None, 30, 'Planificación', 30, proyecto.id])

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
                None, None, 30, 'Cancelado', 30, proyecto.id])