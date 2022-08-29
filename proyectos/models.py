from django.db import models
import sys
sys.path.append("..")
from usuarios.models import Usuario

# Create your models here.

class Proyecto(models.Model):
    #El id se genera de forma automática
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200) #Usado CharField para compatibilidad con el formulario html
    fechaInicio = models.DateTimeField() #Incluye minutos y segundos
    fechaFin = models.DateTimeField()
    idScrumMaster = models.ForeignKey(Usuario, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=30)
    # TODO: Añadir método para convertir a string


# Participante de un proyecto (separado de usuario)
class Participante(models.Model):
    # El id se genera de modo automático
    idProyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE) # Se elimina el proyecto, se eliminan sus participantes
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) # Si borramos el usuario, se borran todas sus participaciones
    #rol = models.ForeignKey(Rol_Interno, on_delete=models.PROTECT) Si borramos un rol interno, ¿qué ocurre con los usuarios que tienen ese rol?
    # TODO: Añadir método para convertir a string













