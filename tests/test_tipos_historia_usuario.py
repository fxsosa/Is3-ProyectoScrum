import pytest
from django.db import models
from historiasDeUsuario.models import Tipo_Historia_Usuario
from historiasDeUsuario.models import Columna_Tipo_Historia_Usuario
from datetime import datetime
from proyectos.models import Proyecto
from usuarios.models import Usuario




@pytest.mark.django_db
def test_crear_tipo_HU():
    # Obtener fecha y hora actuales
    user = Usuario.objects.create(email='user@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                       fechaInicio=None, fechaFin=None, scrumMaster=user, estado='Creado')

    # instancia_tipo_HU = Tipo_Historia_Usuario.objects.get(id=1)
    ahora = datetime.now()
    cadena_ahora = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fechaCreacion = cadena_ahora

    instancia_tipo_HU = Tipo_Historia_Usuario(nombre='TipoHU', fechaCreacion=fechaCreacion)
    instancia_tipo_HU.save()
    instancia_tipo_HU.proyecto.add(proyecto)

    assert instancia_tipo_HU.__str__() == str(['TipoHU', fechaCreacion, instancia_tipo_HU.proyecto])

    instancia_tipo_HU.delete()

@pytest.mark.django_db
def test_crear_columna_tipo_HU():
    user = Usuario.objects.create(email='user@gmail.com', username='Username', nombres='Nombres del Usuario',
                                  apellidos='Apellidos del Usuario', is_staff=False, is_active=True)
    proyecto = Proyecto.objects.create(nombre='Proyecto 1', descripcion='Descripcion 1',
                                             fechaInicio=None, fechaFin=None, scrumMaster=user, estado='Creado')

    #instancia_tipo_HU = Tipo_Historia_Usuario.objects.get(id=1)
    ahora = datetime.now()
    cadena_ahora = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fechaCreacion = cadena_ahora

    instancia_tipo_HU = Tipo_Historia_Usuario(nombre='TipoHU', fechaCreacion=fechaCreacion)
    instancia_tipo_HU.save()
    instancia_tipo_HU.proyecto.add(proyecto)

    col = Columna_Tipo_Historia_Usuario(nombre='nombre',  # Crear columna
                                        orden=1,
                                        tipoHU=instancia_tipo_HU)

    assert col.__str__() == str([instancia_tipo_HU, 'nombre', 1])

    instancia_tipo_HU.delete()
