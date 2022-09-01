from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from proyectos.models import ManejoProyectos

# Create your views here.
# Vista con forms
'''def crearProyecto(request):
    if request.method == 'POST':
        form = CrearProyectoForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('proyectoCreado.html')
    else:
        form = CrearProyectoForm()

    return render(request, 'proyectos/templates/crearProyecto.html', {'form': form})
'''


def crearProyectoPost(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        fechaInicio = request.POST['fechaInicio']
        fechaFin = request.POST['fechaFin']
        scrumMaster= request.POST['scrumMaster']
        estado = request.POST['estado']

        ManejoProyectos.crearProyecto(nombre=nombre, descripcion=descripcion,
                                      fechaInicio=fechaInicio, fechaFin=fechaFin,
                                      scrumMaster=scrumMaster, estado=estado)


    return HttpResponse('<h1>Proyecto creado</h1>')






