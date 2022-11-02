import pytest
import pytz
from django.db import models
from historiasDeUsuario.models import Tipo_Historia_Usuario
from historiasDeUsuario.models import Columna_Tipo_Historia_Usuario
from datetime import datetime
from proyectos.models import Proyecto
from usuarios.models import Usuario




@pytest.mark.django_db
def test_crear_tipo_HU():
    # Obtener fecha y hora actuales
    user = Usuario.objects.create(email='user@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                       fechaInicio=None, fechaFin=None, scrumMaster=user, estado='Creado')

    instancia_tipo_HU = Tipo_Historia_Usuario(nombre='TipoHU')
    instancia_tipo_HU.save()
    instancia_tipo_HU.proyecto.add(proyecto)
    assert instancia_tipo_HU.__str__() == str(['TipoHU', instancia_tipo_HU.proyecto])
    instancia_tipo_HU.delete()


@pytest.mark.django_db
def test_actualizarTipoHU():
    auxDateTime1 = datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.create(nombre='StableDiffusion',
                                       descripcion='IA para generación de imágenes',
                                       fechaInicio=auxDateTime1, fechaFin=auxDateTime2,
                                       scrumMaster=user1, estado='creado')

    tipoHU = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Tipo 1", "id_proyecto": proyecto.id,
                                                        "columnas": ["To Do", "Doing", "Done"]})

    confirmacion = Tipo_Historia_Usuario.objects.actualizarTipoHU({"nombre": "Nombre Actualizado",
                                                                        "id": tipoHU.id})

    # Verificando la confirmacion
    assert confirmacion is True, "Error al actualizar un Tipo de Historia de Usuario"


@pytest.mark.django_db
def test_borrarTipoHU():
    auxDateTime1 = datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.create(nombre='StableDiffusion',
                                       descripcion='IA para generación de imágenes',
                                       fechaInicio=auxDateTime1, fechaFin=auxDateTime2,
                                       scrumMaster=user1, estado='creado')

    tipoHU = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Tipo 1", "id_proyecto": proyecto.id,
                                                        "columnas": ["To Do", "Doing", "Done"]})

    confirmacion = Tipo_Historia_Usuario.objects.borrarTipoHU(id=tipoHU.id)

    # Verificamos si se confirma el borrado
    assert confirmacion is True, "Error al borrar un tipo de historia de usuario"


@pytest.mark.django_db
def test_importarTipoHU():
    auxDateTime1 = datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    user1 = Usuario.objects.create_user(email='user@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto = Proyecto.objects.create(nombre='StableDiffusion',
                                       descripcion='IA para generación de imágenes',
                                       fechaInicio=auxDateTime1, fechaFin=auxDateTime2,
                                       scrumMaster=user1, estado='creado')

    tipoHU = Tipo_Historia_Usuario.objects.crearTipoHU({"nombre": "Tipo a importar", "id_proyecto": proyecto.id,
                                                        "columnas": ["To Do", "Doing", "Done"]})

    auxDateTime1 = datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    user2 = Usuario.objects.create_user(email='user2@email.com', password='abcdefg',
                                        nombres='Nombre1 Nombre2', username='Username 1',
                                        apellidos='Apellido1 Apellido2', )

    proyecto2 = Proyecto.objects.create(nombre='StableDiffusion 2',
                                       descripcion='IA para generación de imágenes',
                                       fechaInicio=auxDateTime1, fechaFin=auxDateTime2,
                                       scrumMaster=user1, estado='creado')

    Tipo_Historia_Usuario.objects.importarTipoHU({"id_proyecto": proyecto2.id,
                                                  "id_tipo_HU": tipoHU.id})

    # Verificamos que el tipo de US del proyecto 2 es el tipo importado del proyecto 1
    tipoHU2 = Tipo_Historia_Usuario.objects.filter(proyecto=proyecto2)
    tipoHU2 = tipoHU2[0]
    assert str([tipoHU2.nombre, tipoHU2.proyecto.filter(id=proyecto2.id).exists()]) == str(["Tipo a importar", True])

@pytest.mark.django_db
def test_crear_columna_tipo_HU():
    user = Usuario.objects.create(email='user@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user, estado='Creado')

    #instancia_tipo_HU = Tipo_Historia_Usuario.objects.get(id=1)
    ahora = datetime.now()
    cadena_ahora = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fechaCreacion = cadena_ahora

    instancia_tipo_HU = Tipo_Historia_Usuario(nombre='TipoHU', fechaCreacion=fechaCreacion)
    instancia_tipo_HU.save()
    instancia_tipo_HU.proyecto.add(proyecto)

    col = Columna_Tipo_Historia_Usuario(nombre='nombre',  # Crear columna
                                        orden=1,
                                        tipoHU=instancia_tipo_HU)

    assert col.__str__() == str([instancia_tipo_HU, 'nombre', 1])

    instancia_tipo_HU.delete()
