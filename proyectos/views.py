from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms # Para crear proyecto

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







