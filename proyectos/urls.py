from app import views as myapp_views
from django.urls import path, include
from proyectos.controllers import controllerProyecto, controllerProyectos,ControllerProyectoParticipantes, \
controllerProyectosInicio, controllerProyectosImportar, ControllerRolesProyectosUsuarios
from rest_framework.urlpatterns import format_suffix_patterns

# Url para proyectos en singular, con funciones para hacer GET y POST con un proyecto
urlpatterns = [
    path('', controllerProyecto.as_view(), name="proyecto"),
    path('listar-participantes', ControllerProyectoParticipantes.as_view(), name="participantes"),
    path('iniciarProyecto', controllerProyectosInicio.as_view(), name="inicioProyecto"),
    path('importar_roles', controllerProyectosImportar.as_view(), name='importar_roles'),
    path('usuario/roles-internos', ControllerRolesProyectosUsuarios.as_view(), name='obtener_roles'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
