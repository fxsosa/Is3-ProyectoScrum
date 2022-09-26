from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def vue_test(request):
    return render(request, 'myapp/index.html')