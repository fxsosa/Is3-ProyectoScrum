import pytest
import pytz

from proyectos.models import Proyecto
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
















