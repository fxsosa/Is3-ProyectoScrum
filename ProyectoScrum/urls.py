# from django.contrib import admin
from django.urls import path, include
from app import views as myapp_views
from django.contrib import admin
# from django.contrib import admin

urlpatterns = [
    path('api/v1/usuario/', include('usuarios.urls')),
    path('api/v1/proyecto/', include('proyectos.urls')),
    path('api/v1/proyectos/', include('proyectos.urls2')),
    path('', myapp_views.vue_test),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/tipoHistoriaUsuario/', include('historiasDeUsuario.urls')),
    path('api/v1/participantes/', include('proyectos.urls3')),
    path('api/v1/rol/', include('roles.urls')),
]


