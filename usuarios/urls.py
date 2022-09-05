from app import views as myapp_views
from django.urls import path, include
from usuarios.controllers import controllerProyecto, ControllerUsuarioAdministracion
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerProyecto.as_view(), name="usuario"),
    path('/admin', ControllerUsuarioAdministracion.as_view(), name="admin"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
