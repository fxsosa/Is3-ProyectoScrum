from app import views as myapp_views
from django.urls import path, include
from roles.controllers import ListaRoles, RolExterno, RolInterno
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('/listarrol', ListaRoles.as_view(), name="listarrol"),
    path('/interno', RolInterno.as_view(), name="interno"),
    path('/externo', RolExterno.as_view(), name="externo"),
]

urlpatterns = format_suffix_patterns(urlpatterns)