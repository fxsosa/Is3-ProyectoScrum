from app import views as myapp_views
from django.urls import path, include
from usuarios.controllers import controllerProyecto
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', controllerProyecto.as_view(), name="usuario"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
