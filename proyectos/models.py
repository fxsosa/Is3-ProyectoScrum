from django.db import models
from usuarios.models import Usuario
# Create your models here.

class Proyecto(models.Model):
    #El id se genera de forma automática
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(max_length=200)#descripcion text o char 200
    fechaInicio = models.DateTimeField() #Incluye minutos y segundos
    fechaFin = models.DateTimeField()
    idScrumMaster = models.ForeignKey(Usuario, on_delete=models.SET_NULL)#idScrumMaster usuario
    estado = model.CharField(max_length=30) #char 30
    # TODO: Añadir tipos de historia de usuarios permitidas
    # TODO: Añadir roles de los participantes
    # TODO: ¿Añadir sprint inicial? ¿o sprint en general?
    # TODO:












