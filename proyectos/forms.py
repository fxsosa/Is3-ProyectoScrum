from django import forms

class CrearProyectoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del proyecto:', max_length=80)
    descripcion = forms.CharField(label='Descripción:', max_length=200)
    fechaInicio = forms.DateTimeField(label='Fecha de inicio:')  # Incluye minutos y segundos
    fechaFin = forms.DateTimeField(label='Fecha de finalización:')
    idScrumMaster = forms.ForeignKey(label='Id de usuario:')
    estado = forms.CharField(label='Estado del proyecto', max_length=30)
    #TODO: Averiguar cómo delimitar a las 5 categorías su estado
