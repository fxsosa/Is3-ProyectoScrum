from django.db import models


# Create your models here.
class RolExterno(models.Model):
    nombre = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str([self.nombre])
