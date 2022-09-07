from app import views as myapp_views
from django.urls import path, include
from proyectos.controllers import controllerParticipantes
from rest_framework.urlpatterns import format_suffix_patterns

# Url para proyectos en plural, con funciones como obtener todos los proyectos
urlpatterns = [
    path('', controllerParticipantes.as_view(), name="participantes")
]

urlpatterns = format_suffix_patterns(urlpatterns)