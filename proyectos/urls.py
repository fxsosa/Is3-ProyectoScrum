from django.urls import path

from . import views

urlpatterns = [
    path('/crearProyecto', views.crearProyecto())
]
