import pytest
from roles.models import Rol


@pytest.mark.django_db
def test_rol_externo():
    rol = Rol.objects.crearRolExterno(nombre='Rol_Prueba', descripcion='Description Prueba')

    assert rol.__str__() == str([rol.nombre])


@pytest.mark.django_db
def test_rol_interno():
    rol = Rol.objects.crearRolInterno(nombre='Rol_Prueba 2', descripcion='Description de prueba')

    assert rol.__str__() == str([rol.nombre])
