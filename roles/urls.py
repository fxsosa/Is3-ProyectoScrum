from app import views as myapp_views
from django.urls import path, include
from roles.controllers import ListaRoles, Rol, usuarioRoles
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('/listar', ListaRoles.as_view(), name="listar"),
    path('', Rol.as_view(), name="crear"),
    path('/usuario', usuarioRoles.as_view(), name="usuario"),
]

urlpatterns = format_suffix_patterns(urlpatterns)