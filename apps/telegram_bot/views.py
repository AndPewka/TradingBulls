from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def dynamic_graph(request):
    return render(request, 'dynamic_graph.html')