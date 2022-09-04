from app import views as myapp_views
from django.urls import path, include
from roles.controllers import ListaRoles, Rol
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('/listar', ListaRoles.as_view(), name="listar"),
    path('', Rol.as_view(), name="crear"),
]

urlpatterns = format_suffix_patterns(urlpatterns)