# from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.views.generic import TemplateView
from app import views as myapp_views
from app import models
from django.contrib import admin
# from django.contrib import admin

urlpatterns = [
    path('saludos/', models.a),
    path('', myapp_views.vue_test),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/rol', include('roles.urls')),
]
