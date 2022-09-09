from app import views as myapp_views
from django.urls import path, include
from historiasDeUsuario.controllers import controllerTipoHU
from rest_framework.urlpatterns import format_suffix_patterns

# Url para proyectos en singular, con funciones para hacer GET y POST con un proyecto

urlpatterns = [
    path('', controllerTipoHU.as_view(), name="proyecto"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
