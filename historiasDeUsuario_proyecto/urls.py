from app import views as myapp_views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from historiasDeUsuario_proyecto.controllers import HistoriaUsuario, ListaHistoriasUsuario, ListaHUTipo

urlpatterns = [
    path('listar', ListaHistoriasUsuario.as_view(), name="listar"),
    path('', HistoriaUsuario.as_view(), name="historiaUsuario"),
    path('listar-por-tipo', ListaHUTipo.as_view(), name="listarHUTipo")
]

urlpatterns = format_suffix_patterns(urlpatterns)
