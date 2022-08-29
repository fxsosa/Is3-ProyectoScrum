from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

def crearProyecto(request):
    if request.method == 'POST':
        form = CrearProyectoForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('')
    else:
        form = CrearProyectoForm()

    return render(request, 'crearProyecto.html', {'form': form})