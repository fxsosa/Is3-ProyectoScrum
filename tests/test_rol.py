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
    user = Usuario.objects.create(email='user@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre de prueba", descripcion='Descripcion de prueba',
                                      idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre de Prueba', descripcion='Descripcion de Prueba')

    assert str(rolInterno.rolGrupo.name) == Rol.objects.obtenerNombreGrupo(rolInterno), "El nombre del grupo de Rol Interno no coincide con el esperado"
    assert str(rolExterno.rolGrupo.name) == Rol.objects.obtenerNombreGrupo(rolExterno), "El nombre del grupo de Rol Exsterno no coincide con el esperado"


@pytest.mark.django_db
def test_listarUsuarios():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    Rol.objects.asignarRolaUsuario(idRol=rolInterno.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rolInterno.id, user=user2)
    Rol.objects.asignarRolaUsuario(idRol=rolExterno.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rolExterno.id, user=user2)
    queryListInterno = Rol.objects.listarUsuarios(nombreRol='Nombre Rol Interno')
    queryListExterno = Rol.objects.listarUsuarios(nombreRol='Nombre Rol Externo')
    assert str([queryListInterno[0].email, queryListInterno[1].email]) == str(['user1@gmail.com', 'user2@gmail.com']), "Error al obtener lista de usuarios con Rol Interno"
    assert str([queryListExterno[0].email, queryListExterno[1].email]) == str(['user1@gmail.com', 'user2@gmail.com']), "Error al obtener lista de usuarios con Rol Externo"


@pytest.mark.django_db
def test_listarRoles():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario', apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba', idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')
    lista = Rol.objects.listarRoles()
    assert str(list(lista)) == str([rolInterno, rolExterno]), "Error al listar todos los roles del sistema"


@pytest.mark.django_db
def test_listarRolesPorUsuario():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno1 = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolInterno2 = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                              idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    Rol.objects.asignarRolaUsuario(idRol=rolInterno1.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rolInterno2.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rolExterno.id, user=user1)

    assert str(Rol.objects.listarRolesPorUsuario(userEmail='user1@gmail.com')) == \
           str([rolInterno1.id, rolInterno2.id, rolExterno.id])

@pytest.mark.django_db
def test_asignarRolaUsuario():
    assert True

@pytest.mark.django_db
def test_eliminarRolaUsuario():
    assert True

@pytest.mark.django_db
def test_existeRol():
    assert True

@pytest.mark.django_db
def test_existeRolId():
    assert True

@pytest.mark.django_db
def test_agregarPermisoDeObjeto():
    assert True


@pytest.mark.django_db
def test_agregarListaPermisoObjeto():
    assert True

@pytest.mark.django_db
def test_agregarPermisoGlobal():
    assert True

@pytest.mark.django_db
def test_agregarListaPermisoGlobal():
    assert True

@pytest.mark.django_db
def test_borrarListaPermisoGlobal():
    assert True

@pytest.mark.django_db
def test_borrarListaPermisoObjeto():
    assert True

@pytest.mark.django_db
def test_borrarRol():
    assert True

@pytest.mark.django_db
def test_listarRolesInternos():
    assert True

@pytest.mark.django_db
def test_listarRolesExternos():
    assert True

@pytest.mark.django_db
def test_listarPermisos():
    assert True

@pytest.mark.django_db
def test_listarRolesExternos():
    assert True

@pytest.mark.django_db
def test_listarRolesExternos():
    assert True
