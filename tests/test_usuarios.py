import pytest
from django.contrib.auth import get_user_model
from roles.models import Rol_Externo


# Obs.: Definido para acceder a la base de datos


@pytest.mark.django_db
def test_usuario_con_rol():
    rol = Rol_Externo.objects.create(nombre='Rol_Prueba')
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', rol=rol,)

    assert user1.__str__() == str([user1.email, user1.nombres, user1.apellidos, user1.rol.nombre])

@pytest.mark.django_db
def test_usuario_sin_rol():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2', rol=None,)

    assert user1.__str__() == str([user1.email, user1.nombres, user1.apellidos, None])