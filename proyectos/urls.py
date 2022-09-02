from app import views as myapp_views
from django.urls import path, include
from proyectos.controllers import controllerProyecto, controllerProyectos
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerProyecto.as_view(), name="proyecto"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
