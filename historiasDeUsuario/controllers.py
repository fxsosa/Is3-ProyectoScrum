from django.http import HttpResponse
from rest_framework.views import APIView
from django.core import serializers

from historiasDeUsuario.models import Tipo_Historia_Usuario, Columna_Tipo_Historia_Usuario


class controllerTipoHU(APIView):

    # Esta función serviría para obtener un tipo de HU en particular (falta testear)
    def get(self, request):
        try:
            id=request.GET.get('q', '') #Recibe el parámetro "q" de la url
            tipo_HU = Tipo_Historia_Usuario.objects.get(id=int(id))
            print(tipo_HU)

            # Obtener todas las columnas de la HU
            columnas = Columna_Tipo_Historia_Usuario.objects.retornarColumnas(id)
            lista_total= []

            lista_total.append(tipo_HU)

            for elemento in columnas:
                lista_total.append(elemento)

            serializer = serializers.serialize('json', lista_total)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    # Retorna todos los tipos de HU en la base de datos (funciona perfectamente)
    '''def get(self, request):
        try:
            tiposHU = Tipo_Historia_Usuario.objects.all()
            serializer = serializers.serialize('json', tiposHU)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)
        '''

    # El POST va a crear directamente un tipo de HU
    # con su proyecto asociado
    def post(self, request):
        try:
            datos = request.data
            tipoHU = Tipo_Historia_Usuario.objects.crearTipoHU(datos)

            return HttpResponse(tipoHU, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    #TODO: Crear opción para importar HU en un proyecto
    # Put usado para añadir HU a proyectos
    '''def put(self, request):
        try:
            datos = request.data
            proyecto = Proyecto.objects.modificarProyecto(datos)

            return HttpResponse(proyecto, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)
        '''



