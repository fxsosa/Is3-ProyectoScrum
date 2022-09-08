from app import views as myapp_views
from django.urls import path, include
from proyectos.controllers import controllerProyecto, controllerProyectos,ControllerProyectoParticipantes
from rest_framework.urlpatterns import format_suffix_patterns

# Url para proyectos en singular, con funciones para hacer GET y POST con un proyecto

urlpatterns = [
    path('', controllerProyecto.as_view(), name="proyecto"),
    path('/listar-participantes', ControllerProyectoParticipantes.as_view(), name="participantes"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
