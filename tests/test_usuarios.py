import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_usuario_con_rol():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)

    assert user1.__str__() == str([user1.email, user1.username, user1.nombres, user1.apellidos])

@pytest.mark.django_db
def test_usuario_sin_rol():
    User = get_user_model()
    user1 = User.objects.create_user(email='user@email.com', password='abcdefg', username='username1', nombres='Nombre1 Nombre2', apellidos='Apellido1 Apellido2',)

    assert user1.__str__() == str([user1.email, user1.username, user1.nombres, user1.apellidos])
