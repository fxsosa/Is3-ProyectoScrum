# from django.contrib import admin
from django.urls import path, include
from app import views as myapp_views
from django.contrib import admin

urlpatterns = [
    path('api/v1/usuario', include('usuarios.urls')),
    path('', myapp_views.vue_test),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]


