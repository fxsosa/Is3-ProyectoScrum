from django.db import models
from datetime import datetime
import pytz
from proyectos.models import Proyecto

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
        instanciaTipoHU = self.model(nombre=nombre)
        instanciaTipoHU.save()
        # Añadir el tipo de HU a un proyecto individual
        proyecto = Proyecto.objects.get(id=int(datos['id_proyecto']))
        instanciaTipoHU.proyecto.add(proyecto)
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

        instanciaTipoHU.save()
        return instanciaTipoHU

    def actualizarTipoHU(self, datos):
        """Función para actualizar un tipo de Historia de Usuario
            
            :param datos: datos del request
            :return: null
        """

        tipoHU = Tipo_Historia_Usuario.objects.get(id=datos['id'])
        tipoHU.nombre = datos['nombre']
        tipoHU.save()
        return True


    def borrarTipoHU(self, id):
        """
            Función para borrar un tipo de Historia de Usuario
            :param datos: datos del request
            :return: null
        """

        # Evitamos borrar el tipo de HU si está en algún Sprint Backlog
        from sprints.models import SprintBacklog # Importando así evitamos el error de "importe circular"

        lista_backlog = SprintBacklog.objects.all()
        lista_tipo_hu_id = []

        # Obtenemos todas las id de los tipos de HU presentes en los Sprint Backlog
        for backlog in lista_backlog:
            lista_hu = backlog.historiaUsuario.all()
            for hu in lista_hu:
                lista_tipo_hu_id.append(hu.tipo_historia_usuario.id)

        print('Lista:')
        print(lista_tipo_hu_id)
        # Si el tipo de HU que se desea eliminar existe en un Sprint Backlog entonces no puede ser eliminado
        for id_tipo_hu in lista_tipo_hu_id:
            if int(id) == id_tipo_hu:
                return False


        tipoHU = Tipo_Historia_Usuario.objects.get(id=id)
        tipoHU.delete()
        return True


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

        tipo_HU_nuevo.proyecto.add(proyecto)


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
        lista_columnas_tipo_HU = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=id_tipo_HU).order_by('orden'))
        if len(lista_columnas_tipo_HU) == 0:
            orden_columna = 1
        else:
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
        lista_columnas_tipo_HU = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=id_tipo_HU).order_by('orden'))

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

            print("lista_columnas_tipo_HU",lista_columnas_tipo_HU)
            print("columna_origen", columna_origen)
            print("columna_destino", columna_destino)

            # Intercambio

            aux_orden = columna_origen.orden
            columna_origen.orden = columna_destino.orden
            columna_destino.orden = aux_orden

            columna_origen.save()
            columna_destino.save()

            return "Se ha realizado el intercambio exitosamente"

    def eliminarColumna(self, datos):
        """
        Elimina una columna de un tipo de HU
        :param datos:
        orden: Recibe un orden numérico
        :return:
        """
        from sprints.models import SprintBacklog  # Importando así evitamos el error de "importe circular"


        id_tipo_HU = datos['id_tipo_HU']
        orden = datos['orden']
        indice_orden = orden - 1


        lista_columnas_tipo_HU = list(Columna_Tipo_Historia_Usuario.objects.filter(tipoHU_id=id_tipo_HU).order_by('orden'))
        orden_maximo = lista_columnas_tipo_HU[-1].orden
        indice_orden_maximo = orden_maximo - 1




        # TODO: Evitar borrar columna si tiene una HU ahí


        # Se evita borrar una columna si tiene HU en esa posición
        lista_backlog = SprintBacklog.objects.all()
        lista = []

        for backlog in lista_backlog:
            lista_hu = backlog.historiaUsuario.all()
            for hu in lista_hu:
                if hu.tipo_historia_usuario.id == int(id_tipo_HU):
                    lista.append(hu)

        # Se maneja el orden como cadena para el frontend
        if orden == orden_maximo:
            estado_col_a_borrar = "finalizada"
        else:
            estado_col_a_borrar = str(orden)

        for hu in lista: # Si existe una HU en la columna, entonces no podemos borrarla
            if hu.estado == estado_col_a_borrar:
                return False


        #Proceso de borrado
        if(indice_orden == indice_orden_maximo):
            columna = lista_columnas_tipo_HU[indice_orden_maximo]
            columna.delete()
        else:
            columna = lista_columnas_tipo_HU[indice_orden]
            columna.delete()

            # Actualizar orden de las columnas a la derecha
            for indice in range(indice_orden+1, orden_maximo):
                columna = lista_columnas_tipo_HU[indice]
                columna.orden = columna.orden - 1
                columna.save()

        return True



class Tipo_Historia_Usuario(models.Model):
    """
        Clase de un Tipo de Historia de Usuario
    """
    nombre = models.CharField(max_length=80)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    proyecto = models.ManyToManyField(Proyecto)

    objects = ManejoTipoHU()

    def __str__(self):
        return str([self.nombre, self.proyecto])

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




