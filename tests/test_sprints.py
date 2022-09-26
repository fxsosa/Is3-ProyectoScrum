import pytest
import pytz

from sprints.models import Sprint, SprintEquipo, SprintBacklog
from usuarios.models import Usuario
from django.contrib.auth import get_user_model
import datetime

@pytest.mark.django_db
def test_Sprint():
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    sprint = Sprint.objects.create(fecha_inicio=auxDateTime1, fecha_fin=auxDateTime2, capacidadEquipo=84, estado='Creado')

    assert sprint.__str__() == str([sprint.fecha_inicio, sprint.fecha_fin, sprint.capacidadEquipo, sprint.estado])


@pytest.mark.django_db
def test_SprintBacklog():
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    sprint = Sprint.objects.create(fecha_inicio=auxDateTime1, fecha_fin=auxDateTime2, capacidadEquipo=84, estado='Creado')
    sprintBacklog = SprintBacklog.objects.create(idSprint=sprint)

    assert sprintBacklog.__str__() == str([sprint.id])


@pytest.mark.django_db
def test_SprintEquipo():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', nombres='Nombre1 Nombre2', username='Username 1', apellidos='Apellido1 Apellido2',)
    auxDateTime1 = datetime.datetime(2022, 8, 10, 8, 00, 00, tzinfo=pytz.UTC)
    auxDateTime2 = datetime.datetime(2022, 12, 10, 17, 00, 00, tzinfo=pytz.UTC)
    sprint = Sprint.objects.create(fecha_inicio=auxDateTime1, fecha_fin=auxDateTime2, capacidadEquipo=84, estado='Creado')

    equipo = SprintEquipo.objects.create(usuario=user1, sprint=sprint, trabajo='Trabajo 1', capacidad=84)

    assert equipo.__str__() == str([equipo.usuario.id, equipo.sprint.id, equipo.trabajo,
                    equipo.capacidad.__str__()])

