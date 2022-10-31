import pytest
import pytz
from proyectos.models import Proyecto, participante
from roles.models import Rol
from usuarios.models import Usuario
import datetime

@pytest.mark.django_db
def test_Proyecto():
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                     nombres='Nombre1 Nombre2', username='Username 1',
                                     apellidos='Apellido1 Apellido2',)

    proyecto = Proyecto.objects.create(nombre='StableDiffusion',
                                       descripcion='IA para generación de imágenes',
                                       fechaInicio=auxDateTime1, fechaFin=auxDateTime2,
                                       scrumMaster=user1,estado='creado')

    assert proyecto.__str__() == str([proyecto.nombre, proyecto.descripcion,
                                      proyecto.fechaInicio, proyecto.fechaFin,
                                      proyecto.scrumMaster.id, proyecto.estado])


@pytest.mark.django_db
def test_crearProyecto():
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    assert str([proyecto.nombre, proyecto.descripcion, proyecto.fechaInicio, proyecto.fechaFin,
                proyecto.scrumMaster, proyecto.estado]) == str(["Nombre Proyecto",
                                                                "Descripcion Proyecto",
                                                                None, None, user1,
                                                                "planificación"]), "Error al crear un proyecto"

@pytest.mark.django_db
def test_ModificarProyecto():
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    # Actualizamos el nombre y descripcion
    Proyecto.objects.modificarProyecto({"id": proyecto.id, "nombre": "Nombre Actualizado",
                                        "descripcion": "Descripcion Actualizada"})

    # Verificamos los cambios
    proyectoActualizado = Proyecto.objects.get(id=proyecto.id)
    assert str([proyectoActualizado.nombre, proyectoActualizado.descripcion]) == str(["Nombre Actualizado", "Descripcion Actualizada"]), "Error al actualizar los datos de un proyecto"

@pytest.mark.django_db
def test_iniciarProyecto():
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    Proyecto.objects.iniciarProyecto({"id": proyecto.id})

    proyecto = Proyecto.objects.get(id=proyecto.id)
    # Verificamos que el proyecto tenga el estado iniciado
    assert proyecto.estado == "iniciado", "Error al iniciar proyecto"


@pytest.mark.django_db
def test_importarRoles():
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto Original",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    rol = Rol.objects.crearRolInterno(nombre="Rol a Importar", descripcion='Descripcion de Prueba', idProyecto=proyecto.id)

    proyecto2 = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto Original",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    rolImportado = Proyecto.objects.importarRoles({"idProyectoActual": proyecto2.id, "idProyectoExterno": proyecto.id, "idRol":  rol.id})

    # Verificamos los datos sean los correctos (especialmente, que apunte al proyecto 2)
    assert str([rolImportado.nombre, rolImportado.descripcion,
                rolImportado.proyecto]) == str(["Rol a Importar",
                                                "Descripcion de Prueba",
                                                proyecto2]), "Error al importar Rol de proyecto"


@pytest.mark.django_db
def test_crearParticipante():
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto Original",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})


    part = participante.objects.crearParticipante({"idProyecto": proyecto.id, "idUsuario": user1.id})

    # Verificamos los datos del participante creado
    assert str([part.proyecto.id, part.usuario.id]) == str([proyecto.id, user1.id]), "Error al crear participante de proyecto!"


@pytest.mark.django_db
def test_listarProyectosdeParticipante():
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto1 = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto Original",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    part1 = participante.objects.crearParticipante({"idProyecto": proyecto1.id, "idUsuario": user1.id})

    proyecto2 = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto 2",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})
    part2 = participante.objects.crearParticipante({"idProyecto": proyecto2.id, "idUsuario": user1.id})

    listaIDProyectos = participante.objects.listarProyectosdeParticipante(id=user1.id)

    # Verificamos que los ID's coincidan con los de los proyectos 1 y 2 creados
    assert listaIDProyectos.__str__() == str([proyecto1, proyecto2]), "Error al listar los proyectos de los cuales participa un usuario"


@pytest.mark.django_db
def test_listarParticipantedeProyectos():
    user1 = Usuario.objects.create_user(email='user1@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    user2 = Usuario.objects.create_user(email='user2@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto1 = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto Original",
                                               "descripcion": "Descripcion Proyecto",
                                               "fechaInicio": None,
                                               "fechaFin": None,
                                               "scrumMaster": user1.email})

    # Agregamos al proyecto
    part1 = participante.objects.crearParticipante({"idProyecto": proyecto1.id, "idUsuario": user1.id})
    part2 = participante.objects.crearParticipante({"idProyecto": proyecto1.id, "idUsuario": user2.id})

    listaUsuarios = participante.objects.listarParticipantedeProyectos(idProyecto=proyecto1.id)
    # Verificando la lista de usuarios participantes del proyecto
    assert listaUsuarios.__str__() == str([user1, user2]), "Error al listar participantes de un proyecto"


@pytest.mark.django_db
def test_borrarParticipante():
    user1 = Usuario.objects.create_user(email='user1@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto1 = Proyecto.objects.crearProyecto({"nombre": "Nombre Proyecto Original",
                                                "descripcion": "Descripcion Proyecto",
                                                "fechaInicio": None,
                                                "fechaFin": None,
                                                "scrumMaster": user1.email})

    # Agregamos al proyecto
    part1 = participante.objects.crearParticipante({"idProyecto": proyecto1.id, "idUsuario": user1.id})

    # Borramos del proyecto
    participante.objects.borrarParticipante(particip=part1)

    # Verificamos que ya no exista el participante (mediante un query)
    assert participante.objects.filter(proyecto=proyecto1, usuario=user1).exists() is False, "Error al eliminar participante de un proyecto"