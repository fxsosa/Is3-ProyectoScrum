import pytest
from django.contrib.auth import get_user_model
import datetime
import pytz

from historiasDeUsuario.models import Tipo_Historia_Usuario, Columna_Tipo_Historia_Usuario
from historiasDeUsuario_proyecto.models import historiaUsuario
from proyectos.models import Proyecto, participante
from usuarios.models import Usuario


@pytest.mark.django_db
def test_crearHistoriaUsuario():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

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
        "idProyecto": idProyecto,
    }
    historia = historiaUsuario.objects.crearHistoriaUsuario(datos=datos)
    assert historia is not None, "Error al crear historia de usuario"

@pytest.mark.django_db
def test_eliminarHistoriaUsuario():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

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
        "idProyecto": idProyecto,
    }
    historia = historiaUsuario.objects.create(nombre="Nombre Prueba",
                                              descripcion="Descripcion de Prueba",
                                              prioridad_tecnica=1,
                                              prioridad_negocio=2,
                                              estimacion_horas=10,
                                              tipo_historia_usuario=tipo,
                                              desarrollador_asignado=part,
                                              proyecto=proyectoPrueba)
    idHistoria = historia.id
    # Ahora si, borrando
    assert historiaUsuario.objects.eliminarHistoriaUsuario(idProyecto=idProyecto, idHistoria=idHistoria), "Error al borrar una historia de usuario recientemente creada"


@pytest.mark.django_db
def test_actualizarHistoriaUsuario():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

    idTipo = tipo.id
    idUsuario = user1.id
    part = participante.objects.crearParticipante({"idUsuario": idUsuario, "idProyecto": idProyecto})
    idParticipante = part.id
    historia = historiaUsuario.objects.create(nombre="Nombre Prueba", descripcion="Descripcion de Prueba", prioridad_tecnica=1, prioridad_negocio=2, estimacion_horas=10, tipo_historia_usuario=tipo, desarrollador_asignado=part, proyecto=proyectoPrueba)
    actualizado = historiaUsuario.objects.actualizarHistoriaUsuario({"idProyecto": idProyecto,
                                                                     "idHistoria": historia.id, "idParticipante": None,
                                                                     "idTipo": None, "nombre": "Nuevo Nombre",
                                                                     "descripcion": None, "prioridad_tecnica": None,
                                                                     "horas_trabajadas": None,
                                                                     "prioridad_negocio": None,
                                                                     "estimacion_horas": None,
                                                                     "estado": None})
    assert str([actualizado[0].nombre, actualizado[0].descripcion, actualizado[0].prioridad_tecnica, actualizado[0].prioridad_negocio, actualizado[0].estimacion_horas, str(actualizado[0].tipo_historia_usuario.id), str(actualizado[0].desarrollador_asignado.id), str(actualizado[0].proyecto.id)]) == str(["Nuevo Nombre", "Descripcion de Prueba", 1, 2, 10, str(tipo.id), str(part.id), str(proyectoPrueba.id)]), "Error al actualizar la historia de usuario"

@pytest.mark.django_db
def test_obtenerHistoriaUsuario():
    # Creamos la historia de usuario
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

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
        "idProyecto": idProyecto,
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos)
    # Probamos la funcion de obtenerHistoriaUsuario
    historia2 = historiaUsuario.objects.obtenerHistoriaUsuario(idProyecto=idProyecto, idHistoria=historia1[0].id)
    assert str([historia1[0].nombre, historia1[0].descripcion, historia1[0].prioridad_tecnica, historia1[0].prioridad_negocio, historia1[0].estimacion_horas, str(historia1[0].tipo_historia_usuario.id), str(historia1[0].desarrollador_asignado.id), str(historia1[0].proyecto.id)]) == str([historia2[0].nombre, historia2[0].descripcion, historia2[0].prioridad_tecnica, historia2[0].prioridad_negocio, historia2[0].estimacion_horas, str(historia2[0].tipo_historia_usuario.id), str(historia2[0].desarrollador_asignado.id), str(historia2[0].proyecto.id)]), "Error al obtener historias de usuario"

@pytest.mark.django_db
def test_listarHistoriasUsuario():
    # Creamos la historia de usuario
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    idProyecto = proyectoPrueba.id
    tipo = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Nombre Prueba",
                                                      "id_proyecto": idProyecto,
                                                      "columnas": ["Columna 1", "Columna 2", "Columna 3"]})

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
        "idProyecto": idProyecto,
    }
    historia1 = historiaUsuario.objects.crearHistoriaUsuario(datos=datos)
    assert historiaUsuario.objects.listarHistoriasUsuario(idProyecto=idProyecto) is not None, "Error al listar historias de usuario de un proyecto"


@pytest.mark.django_db
def test_listarHUTipo():
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

    Proyecto.objects.iniciarProyecto({"id": proyecto.id})

    listaHU = historiaUsuario.objects.listarHUTipo(idProyecto=proyecto.id, idTipoHU=idTipo)

    # Verificamos que los US del sprint backlog obtenidos, sean del mismo tipo que el tipo creado
    assert str([listaHU[0].tipo_historia_usuario.id, listaHU[1].tipo_historia_usuario.id]) == str([tipo.id, tipo.id]), \
        "Error al listar los US de un Tipo, de un Proyecto"