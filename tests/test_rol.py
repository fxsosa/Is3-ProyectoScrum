import pytest
from django.contrib.auth.models import Group

from proyectos.models import Proyecto
from roles.models import Rol
from usuarios.models import Usuario
from guardian.shortcuts import assign_perm, remove_perm, get_group_perms, get_perms


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
           str([str(rolInterno1.id), str(rolInterno2.id), str(rolExterno.id)]), "Error al listar los roles por usuario"

@pytest.mark.django_db
def test_asignarRolaUsuario():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                              idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    Rol.objects.asignarRolaUsuario(idRol=rolInterno.id, user=user1)
    Rol.objects.asignarRolaUsuario(idRol=rolExterno.id, user=user1)
    assert str(Rol.objects.listarRolesPorUsuario(userEmail='user1@gmail.com'))\
           == str([str(rolInterno.id), str(rolExterno.id)]), "Error al asignar roles a usuario"

@pytest.mark.django_db
def test_existeRol():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    assert Rol.objects.existeRol(nombreRol=rolInterno.nombre) == True, "Error en la verificacion por nombre de si existe o no Rol Interno"
    assert Rol.objects.existeRol(nombreRol=rolExterno.nombre) == True, "Error en la verificacion por nombre si existe o no Rol Externo"

@pytest.mark.django_db
def test_existeRolId():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    assert Rol.objects.existeRolId(id=rolInterno.id) == True, "Error en la verificacion por ID de si existe o no Rol Interno"
    assert Rol.objects.existeRolId(id=rolExterno.id) == True, "Error en la verificacion por ID de si existe o no Rol Externo"


@pytest.mark.django_db
def test_agregarPermisoDeObjeto():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    Rol.objects.agregarPermisoDeObjeto(idRol=rolInterno.id, nombrePermiso='proyectos.actualizar_proyecto', objeto=proyectoPrueba)
    assert list(get_group_perms(rolInterno.rolGrupo, rolInterno.proyecto)) == ['actualizar_proyecto'], "Error al agregar permiso de objeto"


@pytest.mark.django_db
def test_agregarListaPermisoObjeto():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)

    lista = [{"nombre": "proyectos.actualizar_proyecto", "idObjeto": proyectoPrueba.id}]
    Rol.objects.agregarListaPermisoObjeto(r=rolInterno, lista=lista)
    assert list(get_group_perms(rolInterno.rolGrupo, rolInterno.proyecto)) == ['actualizar_proyecto'], "Error al agregar permiso de objeto"


@pytest.mark.django_db
def test_agregarPermisoGlobal():
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')
    Rol.objects.agregarPermisoGlobal(idRol=rolExterno.id, nombrePermiso="roles.crear_rol_externo")
    nombreGrupo = Rol.objects.obtenerNombreGrupo(rolExterno)
    grupo = Group.objects.get(name=nombreGrupo)
    assert list(grupo.permissions.all().values('codename')) == [{"codename": 'crear_rol_externo'}], "Error al agregar permiso global"


@pytest.mark.django_db
def test_agregarListaPermisoGlobal():
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')
    lista = ["roles.crear_rol_externo"]
    Rol.objects.agregarListaPermisoGlobal(r=rolExterno, lista=lista)
    nombreGrupo = Rol.objects.obtenerNombreGrupo(rolExterno)
    grupo = Group.objects.get(name=nombreGrupo)
    assert list(grupo.permissions.all().values('codename')) == [{"codename": 'crear_rol_externo'}], "Error al agregar lista de permiso global"


@pytest.mark.django_db
def test_borrarListaPermisoGlobal():
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')
    lista = ["roles.crear_rol_externo", "roles.listar_roles_externos"]
    Rol.objects.agregarListaPermisoGlobal(r=rolExterno, lista=lista)

    # Aca ocurre el borrado
    Rol.objects.borrarListaPermisoGlobal(r=rolExterno, lista=lista)

    nombreGrupo = Rol.objects.obtenerNombreGrupo(rolExterno)
    grupo = Group.objects.get(name=nombreGrupo)
    assert list(grupo.permissions.all().values('codename')) == [], "Error al borrar lista de permiso global"


@pytest.mark.django_db
def test_borrarListaPermisoObjeto():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1', fechaInicio=None,
                                             fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)

    lista = [{"nombre": "proyectos.actualizar_proyecto", "idObjeto": proyectoPrueba.id},
             {"nombre": "proyectos.borrar_proyecto", "idObjeto": proyectoPrueba.id}]
    Rol.objects.agregarListaPermisoObjeto(r=rolInterno, lista=lista)

    # Aca ocurre el borrado
    Rol.objects.borrarListaPermisoObjeto(r=rolInterno, lista=lista)

    nombreGrupo = Rol.objects.obtenerNombreGrupo(rolInterno)
    grupo = Group.objects.get(name=nombreGrupo)
    assert list(grupo.permissions.all().values('codename')) == [], "Error al borrar lista de permiso de objetos"



@pytest.mark.django_db
def test_borrarRol():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    idInterno = rolInterno.id
    idExterno = rolExterno.id

    # Aca ocurre el borrado
    Rol.objects.borrarRol(idRol=idInterno)
    Rol.objects.borrarRol(idRol=idExterno)
    assert Rol.objects.existeRolId(id=idInterno) == False, "Error al borrar rol interno"
    assert Rol.objects.existeRolId(id=idExterno) == False, "Error al borrar rol externo"

@pytest.mark.django_db
def test_listarRolesInternos():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno1 = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolInterno2 = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                              idProyecto=proyectoPrueba.id)
    l = Rol.objects.listarRolesInternos(proyectoPrueba.id)
    assert [l[0].nombre, l[1].nombre] == [rolInterno1.nombre, rolInterno2.nombre], "Error al listar los roles internos de un proyecto"

@pytest.mark.django_db
def test_listarRolesExternos():
    rolExterno1 = Rol.objects.crearRolExterno(nombre="Nombre Rol Externo", descripcion='Descripcion de prueba')
    rolExterno2 = Rol.objects.crearRolExterno(nombre="Nombre Rol Externo", descripcion='Descripcion de prueba')

    l = Rol.objects.listarRolesExternos()
    assert [l[0].nombre, l[1].nombre] == [rolExterno1.nombre, rolExterno2.nombre], "Error al listar los roles externos del sistema"

@pytest.mark.django_db
def test_listarPermisos():
    user1 = Usuario.objects.create(email='user1@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    user2 = Usuario.objects.create(email='user2@gmail.com', username='Username', nombres='Nombres del Usuario',
                                   apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyectoPrueba = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user1, estado='Creado')
    rolInterno = Rol.objects.crearRolInterno(nombre="Nombre Rol Interno", descripcion='Descripcion de prueba',
                                             idProyecto=proyectoPrueba.id)
    rolExterno = Rol.objects.crearRolExterno(nombre='Nombre Rol Externo', descripcion='Descripcion de Prueba')

    lista = ["roles.crear_rol_externo"]
    Rol.objects.agregarListaPermisoGlobal(r=rolExterno, lista=lista)

    lista = [{"nombre": "proyectos.actualizar_proyecto", "idObjeto": proyectoPrueba.id}]
    Rol.objects.agregarListaPermisoObjeto(r=rolInterno, lista=lista)

    lExterno = Rol.objects.listarPermisos(id=rolExterno.id)
    lInterno = Rol.objects.listarPermisos(id=rolInterno.id)
    assert [str(lExterno[0].codename)] == ["crear_rol_externo"], "Error en listar permisos globales"
    assert [str(lInterno[0].codename)] == ["actualizar_proyecto"], "Error en listar permisos de objetos"
