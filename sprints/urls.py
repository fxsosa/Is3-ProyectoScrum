from django.urls import path
from sprints.controllers import controllerSprint, controllerListarSprints, controllerEquipoSprint
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerSprint.as_view(), name="sprint"),
    path('listar', controllerListarSprints.as_view(), name="listarSprint"),
    path('equipo', controllerEquipoSprint.as_view(), name="equipoSprint")
]

urlpatterns = format_suffix_patterns(urlpatterns)
