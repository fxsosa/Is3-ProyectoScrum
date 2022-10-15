from django.urls import path
from sprints.controllers import controllerSprint, controllerListarSprints, controllerEquipoSprint, \
    controllerSprintBacklog, controllerEstadoSprint, ListaHUTipo, controllerListaTipoHU
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerSprint.as_view(), name="sprint"),
    path('listar', controllerListarSprints.as_view(), name="listarSprint"),
    path('equipo', controllerEquipoSprint.as_view(), name="equipoSprint"),
    path('backlog/', controllerSprintBacklog.as_view(), name="sprintBacklog"),
    path('estado', controllerEstadoSprint.as_view(), name="estadoSprint"),
    path('backlog/listar-por-tipo', ListaHUTipo.as_view(), name="listarHUTipo"),
    path('listar-tipos', controllerListaTipoHU.as_view(), name="listarTipoHU")
]

urlpatterns = format_suffix_patterns(urlpatterns)
