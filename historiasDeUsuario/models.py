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
        Se creará un tipo de HU idéntico y será añadida a ese proyecto.
        :param datos:
        :return :
        """
        tipo_HU_viejo = Tipo_Historia_Usuario.objects.get(id=int(datos['id_tipo_HU']))
        proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))

        # Crea un nuevo tipo de HU en la base de datos
        tipo_HU_nuevo = self.model(nombre=tipo_HU_viejo.nombre, fechaCreacion=tipo_HU_viejo.fechaCreacion)
        tipo_HU_nuevo.save()

        #Añadimos las columnas
        lista_col = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=tipo_HU_viejo.id))
        for i in range(len(lista_col)):
            col_a_copiar = lista_col[i]
            col = Columna_Tipo_Historia_Usuario(nombre=col_a_copiar.nombre,  # Crear columna
                                                orden=col_a_copiar.orden,
                                                tipoHU=tipo_HU_nuevo)
            col.save()

        tipo_HU_nuevo.proyectos.add(proyecto)


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

    def agregarColumna(self, datos):
        """
            Función que añade una columna a un tipo de HU existente
        :param datos:
        :return:
        """
        nombre = datos['nombre']  # Una lista de nombres
        id_tipo_HU = datos['id_tipo_HU']
        instancia_tipo_HU = Tipo_Historia_Usuario.objects.get(id=id_tipo_HU)

        #Obtener el nuevo orden de la nueva columna
        lista_columnas_tipo_HU = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=id_tipo_HU))
        orden_columna = lista_columnas_tipo_HU[-1].orden + 1 # Se suma un 1 al orden de la última columna

        col = Columna_Tipo_Historia_Usuario(nombre=nombre,  # Crear columna
                                            orden=orden_columna,
                                            tipoHU=instancia_tipo_HU)
        col.save()

    def modificarColumna(self, datos):
        """
        Método que modifica el nombre de una columna, o intercambia 2 columnas distintas, intercambiando
        nombre y orden
        :param datos:
        :return mensaje: Un mensaje con el resultado de la operación realizada (modificar nombre o intercambiar columnas)
        """
        nombre = datos['nombre']  # Una lista de nombres
        id_tipo_HU = datos['id_tipo_HU']
        orden_origen = datos['orden_origen'] # Estas 2 variables sirven para intercambiar columnas
        orden_destino = datos['orden_destino'] # Pero si son iguales, solo modifica el nombre de la columna objetivo

        # Obtener el nuevo orden de la nueva columna
        lista_columnas_tipo_HU = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=id_tipo_HU))

        if (orden_origen == orden_destino): # Solo modifica el nombre de la columna
            indice_destino = orden_destino - 1 # El orden va de 1 a n, pero los índices van de 0 a n-1

            columna = lista_columnas_tipo_HU[indice_destino]
            columna.nombre = nombre
            columna.save()

            return "Se ha modificado el nombre exitosamente"
        else: # Intercambia columnas (nombre y orden)
            indice_origen = orden_origen - 1
            indice_destino = orden_destino - 1

            columna_origen = lista_columnas_tipo_HU[indice_origen]
            columna_destino = lista_columnas_tipo_HU[indice_destino]

            # Intercambio
            aux_nombre = columna_origen.nombre
            aux_orden = columna_origen.orden
            columna_origen.nombre = columna_destino.nombre
            columna_origen.orden = columna_destino.orden
            columna_destino.nombre = aux_nombre
            columna_destino.orden = aux_orden

            columna_origen.save()
            columna_destino.save()

            #TODO: Migrar US de una columna a otra

            return "Se ha realizado el intercambio exitosamente"

    def eliminarColumna(self, datos):
        """
        Elimina una columna de un tipo de HU
        :param datos:
        :return:
        """
        id_tipo_HU = datos['id_tipo_HU']
        orden = datos['orden']
        indice_orden = orden - 1

        lista_columnas_tipo_HU = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=id_tipo_HU))
        orden_maximo = lista_columnas_tipo_HU[-1].orden
        indice_orden_maximo = orden_maximo - 1

        if(indice_orden == indice_orden_maximo):
            columna = lista_columnas_tipo_HU[indice_orden_maximo]
            columna.delete()
            # TODO: Añadir método para migrar HU de la columna borrada a la siguiente a la izquierda
        else:
            columna = lista_columnas_tipo_HU[indice_orden]
            columna.delete()

            # Actualizar orden de las columnas a la derecha
            for indice in range(indice_orden+1, orden_maximo):
                columna = lista_columnas_tipo_HU[indice]
                columna.orden = columna.orden - 1
                columna.save()



            #TODO: Añadir método para migrar HU de la columna borrada a la siguiente a la derecha







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
    tipoHU = models.ForeignKey(Tipo_Historia_Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=80)
    orden = models.IntegerField()

    objects = ManejoColumasUH()

    def __str__(self):
        return str([self.tipoHU, self.nombre, self.orden])




