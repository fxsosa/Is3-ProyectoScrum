from django.db import models
#import sys
#sys.path.append("..")
from proyectos.models import Proyecto
# Create your models here.
class Tipo_Historia_Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    fechaCreacion = models.DateTimeField()
    proyect = models.ManyToManyField(Proyecto)
    # TODO: Añadir método para convertir a string
