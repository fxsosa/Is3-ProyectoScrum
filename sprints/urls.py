from django.urls import path
from sprints.controllers import controllerSprint, controllerListarSprints, controllerEquipoSprint, \
    controllerSprintBacklog, controllerEstadoSprint
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerSprint.as_view(), name="sprint"),
    path('listar', controllerListarSprints.as_view(), name="listarSprint"),
    path('equipo', controllerEquipoSprint.as_view(), name="equipoSprint"),
    path('backlog/', controllerSprintBacklog.as_view(), name="sprintBacklog"),
    path('estado', controllerEstadoSprint.as_view(), name="estadoSprint")
]

urlpatterns = format_suffix_patterns(urlpatterns)
