from app import views as myapp_views
from django.urls import path, include
from usuarios.controllers import controllerProyecto, \
    ControllerUsuarioAdministracion, \
    ControllerUsuario, \
    ControllerUsuarioIndividualAdmin, \
    ControllerUsuarioExistencia

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ControllerUsuario.as_view(), name="usuario"),
    path('/admin', ControllerUsuarioAdministracion.as_view(), name="admin"),
    path('/proyectos', controllerProyecto.as_view(), name="proyectos"),
    path('/admin/roles', ControllerUsuarioIndividualAdmin.as_view(), name="proyectos"),
    path('/existe', ControllerUsuarioExistencia.as_view(), name="existe"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
