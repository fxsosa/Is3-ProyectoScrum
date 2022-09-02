from django.http import HttpResponse
from rest_framework.views import APIView
from django.core import serializers
from proyectos.models import Proyecto


from proyectos.models import Proyecto

# Para proyectos individuales
class controllerProyecto(APIView):
    def get(self, request): #TODO: Modificar para obtener un proyecto individual
        try:
            proyectos = Proyecto.objects.all()
            serializer = serializers.serialize('json', proyectos)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    def post(self, request):
        try:
            datos = request.data
            proyecto = Proyecto.objects.crearProyecto(datos)
            print(proyecto)

            return HttpResponse(proyecto, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)

    # TODO: Crear función de actualizar proyecto


class controllerProyectos(APIView):
    def get(self, request):
        try:
            proyectos = Proyecto.objects.all()
            serializer = serializers.serialize('json', proyectos)
            return HttpResponse(serializer, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse("Algo salio mal " + str(e), status=500)