from django.db import models

# Create your models here.
class Tipo_Historia_Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    fechaCreacion = models.DateTimeField()
    proyectos = models.ManyToManyField(Proyecto)
    # TODO: Añadir método para convertir a string
