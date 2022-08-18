from django.db import models

# Create your models here.
class Rol_Externo(models.Model):
    nombre = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre
