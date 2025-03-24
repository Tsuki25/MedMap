from django.urls import path
from . import views
from .views import MapaUnidadesView, TriagemCreateView, TriagemUpdateView, LoginView

app_name = 'map'  # Define o namespace do app

urlpatterns = [
    path('', MapaUnidadesView.as_view(), name='mapa'),
    path('triagem/criar/', TriagemCreateView.as_view(), name='triagem_create'),
    path('triagem/<int:pk>/sintomas/', TriagemUpdateView.as_view(), name='triagem_update'),
    path("login/", LoginView.as_view(), name="login"),
]