from django.urls import path
from sprints.controllers import controllerSprint, controllerListarSprints
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerSprint.as_view(), name="sprint"),
    path('listar', controllerListarSprints.as_view(), name="listarSprint"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
