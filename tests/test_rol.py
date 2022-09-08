import pytest

from proyectos.models import Proyecto
from roles.models import Rol
from usuarios.models import Usuario


@pytest.mark.django_db
def test_rol_externo():
    rol = Rol.objects.crearRolExterno(nombre='Nombre de Prueba', descripcion='Descripcion de Prueba')

    assert rol.__str__() == str(["Nombre de Prueba", "Externo", "Descripcion de Prueba", None]), "Error en la declaracion de modelos de rol externo"


@pytest.mark.django_db
def test_rol_interno():
    user = Usuario.objects.create(email='user@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff = False, is_active = True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user, estado='Creado')
    rol = Rol.objects.crearRolInterno(nombre="Nombre de prueba", descripcion='Descripcion de prueba', idProyecto=proyectoPrueba.id)

    assert rol.__str__() == str(["Nombre de prueba", "Interno", "Descripcion de prueba", proyectoPrueba.id]),  "Error en la declaracion de modelos de rol interno"


@pytest.mark.django_db
def test_obtenerNombreGrupo():
    pass

@pytest.mark.django_db
def test_listarUsuarios():
    pass

@pytest.mark.django_db
def test_listarRoles():
    pass

@pytest.mark.django_db
def test_listarRolesPorUsuario():
    pass

@pytest.mark.django_db
def test_asignarRolaUsuario():
    pass

@pytest.mark.django_db
def test_eliminarRolaUsuario():
    pass

@pytest.mark.django_db
def test_existeRol():
    pass

@pytest.mark.django_db
def test_existeRolId():
    pass

@pytest.mark.django_db
def test_agregarPermisoDeObjeto():
    pass


@pytest.mark.django_db
def test_agregarListaPermisoObjeto():
    pass

@pytest.mark.django_db
def test_agregarPermisoGlobal():
    pass

@pytest.mark.django_db
def test_agregarListaPermisoGlobal():
    pass

@pytest.mark.django_db
def test_borrarListaPermisoGlobal():
    pass

@pytest.mark.django_db
def test_borrarListaPermisoObjeto():
    pass

@pytest.mark.django_db
def test_borrarRol():
    pass

@pytest.mark.django_db
def test_listarRolesInternos():
    pass

@pytest.mark.django_db
def test_listarRolesExternos():
    pass

@pytest.mark.django_db
def test_listarPermisos():
    pass

@pytest.mark.django_db
def test_listarRolesExternos():
    pass

@pytest.mark.django_db
def test_listarRolesExternos():
    pass
