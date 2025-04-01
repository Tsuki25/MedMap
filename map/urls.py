from django.urls import path
from . import views
from .views import MapaUnidadesView, TriagemCreateView, TriagemUpdateView, LoginView

app_name = 'map'  # Define o namespace do app

urlpatterns = [
    path('', MapaUnidadesView.as_view(), name='mapa'),
    path('triagem/criar/', TriagemCreateView.as_view(), name='triagem_create'),
    path('triagem/<int:pk>/sintomas/', TriagemUpdateView.as_view(), name='triagem_update'),
    path('mapa/unidades_recomendadas/<int:triagem>', MapaUnidadesView.as_view(), name='mapa_unidades_recomendadas'),
    path('avaliar_unidade/', views.avaliar_unidade_get, name='avaliar_unidade'),
    path("login/", LoginView.as_view(), name="login"),
]