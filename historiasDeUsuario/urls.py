from app import views as myapp_views
from django.urls import path, include
from historiasDeUsuario.controllers import controllerTipoHU, controllerTipoHU_2, controllerColumnasTipoHU
from rest_framework.urlpatterns import format_suffix_patterns

# Url para proyectos en singular, con funciones para hacer GET y POST con un proyecto

urlpatterns = [
    path('', controllerTipoHU.as_view(), name="proyecto"),
    path('tipoHU', controllerTipoHU_2.as_view(), name="tipoHU"),
    path('columnas', controllerColumnasTipoHU.as_view(), name="columnasTipoHU")
]

urlpatterns = format_suffix_patterns(urlpatterns)
