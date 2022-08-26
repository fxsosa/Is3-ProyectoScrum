import pytest
from django.contrib.auth import get_user_model
from roles.models import Rol


@pytest.mark.django_db
def test_usuario_con_rol():
    rol = Rol.objects.crearRolExterno(nombre='Rol Prueba', descripcion='Descripcion de Prueba')
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', rol=rol,)

    assert user1.__str__() == str([user1.email, user1.username, user1.nombres, user1.apellidos, user1.rol.nombre])

@pytest.mark.django_db
def test_usuario_sin_rol():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', rol=None,)

    assert user1.__str__() == str([user1.email, user1.username, user1.nombres, user1.apellidos, None])
