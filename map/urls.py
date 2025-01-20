from django.urls import path
from . import views

app_name = 'map'  # Define o namespace do app

urlpatterns = [
    path('', views.criar_mapa, name='mapa'),
]