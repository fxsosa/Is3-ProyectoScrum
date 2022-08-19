import pytest
from roles.models import RolExterno


@pytest.mark.django_db
def test_rol():
    rol = RolExterno.objects.create(nombre='Rol_Prueba')

    assert rol.__str__() == str([rol.nombre])
