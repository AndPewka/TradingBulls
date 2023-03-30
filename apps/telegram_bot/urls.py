from django.urls import path
from . import views

urlpatterns = [
    path('dynamic_graph/', views.dynamic_graph, name='dynamic_graph'),
]
