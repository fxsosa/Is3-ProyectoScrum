from app import views as myapp_views
from django.urls import path, include
from proyectos.controllers import controllerProyecto, controllerProyectos
from rest_framework.urlpatterns import format_suffix_patterns

# Url para proyectos en plural, con funciones como obtener todos los proyectos
urlpatterns = [
    path('', controllerProyectos.as_view(), name="proyectos")
]

urlpatterns = format_suffix_patterns(urlpatterns)