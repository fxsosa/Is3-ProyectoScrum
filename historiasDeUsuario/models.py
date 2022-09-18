from django.db import models
#import sys
#sys.path.append("..")
from proyectos.models import Proyecto
from datetime import datetime
# Create your models here.


class ManejoTipoHU(models.Manager):
    """
        Manager para manejar tipos de Historias de Usuario
    """

    def crearTipoHU(self, datos):
        """
            Función para crear un tipo de Historia de Usuario
            :param datos: datos del request
            :return: instanciaTipoHU
        """
        nombre = datos['nombre']
        # Obtener fecha y hora actuales
        ahora = datetime.now()
        cadena_ahora = ahora.strftime("%Y-%m-%d %H:%M:%S")
        fechaCreacion = cadena_ahora
        # Añadimos 2 elementos a la instancia de modelo
        instanciaTipoHU = self.model(nombre=nombre, fechaCreacion=fechaCreacion)
        instanciaTipoHU.save()
        # Añadir el tipo de HU a un proyecto individual
        proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))
        instanciaTipoHU.proyectos.add(proyecto)
        instanciaTipoHU.save()

        # Añadir columnas de tipo de HU en orden ascendente (de 1 a n)
        orden_columna=1 # Es el orden de las columnas de un tipo de HU
        columnas = datos['columnas'] # Una lista de nombres
        for nombre in columnas:
            col = Columna_Tipo_Historia_Usuario(nombre=nombre, # Crear columna
                                                orden=orden_columna,
                                                tipoHU=instanciaTipoHU)
            col.save()
            orden_columna=orden_columna+1

        return instanciaTipoHU

    def borrarTipoHU(self, datos):
        """
            Función para borrar un tipo de Historia de Usuario
            :param datos: datos del request
            :return: null
        """
        tipoHU = Tipo_Historia_Usuario.objects.get(id=int(datos['id_tipoUH']))
        tipoHU.delete()


    def importarTipoHU(self, datos):
        """
        Función para importar un tipo de Historia de Usuario a un proyecto determinado.
        La Historia de Usuario será añadida a ese proyecto.
        :param datos:
        :return:
        """
        tipoHU = Tipo_Historia_Usuario.objects.get(id=int(datos['id_tipo_HU']))
        proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))
        print(tipoHU)
        print(proyecto)

        tipoHU.proyectos.add(proyecto)


class ManejoColumasUH(models.Manager):
    """
        Manejar columnas de los tipos de HU
    """
    # Definir función para retornar las columnas de un tipo de UH con cierto id
    def retornarColumnas(self, id_HU):
        """
            Función para retornar las columnas de un tipo de Historia de Usuario
            :param id_HU: id de la Historia de Usuario
            :return: lista_columnas
        """
        columnas_totales = Columna_Tipo_Historia_Usuario.objects.all() #Todas las columnas de la base de datos
        #print(columnas_totales)
        lista_columnas = [] # Columnas que pertenecen a la HU cuyo id recibimos

        for columna in columnas_totales:
            tipoHU = columna.tipoHU
            if tipoHU.id == int(id_HU):
                lista_columnas.append(columna)

        return lista_columnas

class Tipo_Historia_Usuario(models.Model):
    """
        Clase de un Tipo de Historia de Usuario
    """
    nombre = models.CharField(max_length=80)
    fechaCreacion = models.DateTimeField()
    proyectos = models.ManyToManyField(Proyecto)

    objects = ManejoTipoHU()

    def __str__(self):
        return str([self.nombre, self.fechaCreacion, self.proyectos])

    '''
    class Meta:
        #default_permissions = ()  # ?deshabilitamos add/change/delete/view

        permissions = (
            ('crear_tipo_HU', 'Crear un nuevo tipo de Historia de Usuario'),
            ('borrar_tipo_HU', 'Borrar un tipo de HU')
        )
    '''


class Columna_Tipo_Historia_Usuario(models.Model):
    """
        Clase para las columnas de un tipo de Historia de Usuario
    """
    tipoHU = models.ForeignKey(Tipo_Historia_Usuario, on_delete=models.CASCADE) #Evita que se borre, se soluciona borrando el tipo de Historia de Usuario
    nombre = models.CharField(max_length=80)
    orden = models.IntegerField()

    objects = ManejoColumasUH()

    def __str__(self):
        return str([self.idTipoHU, self.nombre, self.orden])




