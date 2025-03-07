from django.shortcuts import render
import folium
from folium.plugins import LocateControl # Usado para pegar a localização do usuário e gerar o ponto

from .models import UnidadeAtendimento
from geopy.distance import geodesic  # Para calcular a distância entre pontos

def criar_mapa(request):
    # Pega as coordenadas do usuárias captadas ao iniciar a aplicação
    lat_user = request.GET.get("lat_user")
    lon_user = request.GET.get("lon_user")

    # Se as coordenadas não forem recebidas, define um valor padrão
    if not lat_user or not lon_user:
        lat_user, lon_user = -23.55, -46.63  # Coordenadas padrão (São Paulo)

    # Converte para float
    coordenadas_usuario = [float(lat_user), float(lon_user)]


    # Criação do mapa centrado no usuário
    mapa = folium.Map(location=coordenadas_usuario, zoom_start=13)

    # Adiciona a Localização do Usuário no mapa
    LocateControl(
        auto_start=True,
        keepCurrentZoomLevel=True,
        drawMarker=True,
        icon="fa-user",  # Define o ícone do usuário
        prefix="fa",  # Define a biblioteca de ícones FontAwesome
        strings={"title": "Sua localização"}  # Define o título do botão
    ).add_to(mapa)

    # Função para adicionar marcadores de unidades no mapa
    def adicionar_ponto_unidade(mapa, latitude, longitude, descricao_completa, cor_marcador):
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(descricao_completa, max_width=300),
            icon=folium.Icon(color=cor_marcador, icon='fa-hospital', prefix='fa')
        ).add_to(mapa)

    # Buscar todas as unidades de atendimento do banco de dados
    unidades = UnidadeAtendimento.objects.all()

    # Lista para armazenar as unidades e suas distâncias do usuário
    unidades_distancia = []

    # Processar cada unidade
    for unidade in unidades:
        # Calcular a distância entre o usuário e a unidade
        coordenadas_unidade = (unidade.endereco.latitude, unidade.endereco.longitude)
        distancia = geodesic(coordenadas_usuario, coordenadas_unidade).km

        # Adicionar à lista de unidades com distância
        unidades_distancia.append({
            "nome": unidade.nome,
            "latitude": unidade.endereco.latitude,
            "longitude": unidade.endereco.longitude,
            "endereco": unidade.endereco.__str__(),
            "planos_saude": ", ".join([convenio.nome_convenio for convenio in unidade.convenios.all()]),
            "horario_atendimento": unidade.horario_atendimento,
            "tempo_medio": unidade.tempo_medio_espera,
            "fila": unidade.lotacao_atual,
            "especialidade": unidade.especialidade,
            "distancia": distancia
        })

    # Ordenar as unidades pela distância e pegar as 5 mais próximas
    unidades_mais_proximas = sorted(unidades_distancia, key=lambda x: x["distancia"])[:5]
    unidades_carregadas = sorted(unidades_distancia, key=lambda x: x["distancia"])[:100]

    # Adicionar os pontos ao mapa para todos as unidades
    for i, unidade in enumerate(unidades_carregadas):
        descricao_completa = f"""
        <div style='width: 200px;'>
            <h4 style='margin-bottom: 10px;'>{unidade['nome']}</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li><strong>Endereço:</strong> {unidade['endereco']}</li>
                <li><strong>Planos de Saúde:</strong> {unidade['planos_saude']}</li>
                <li><strong>Horário:</strong> {unidade['horario_atendimento']}</li>
                <li><strong>Tempo médio:</strong> {unidade['tempo_medio']}</li>
                <li><strong>Fila:</strong> {unidade['fila']}</li>
                <li><strong>Especialidade:</strong> {unidade['especialidade']}</li>
                <li><strong>Distância:</strong> {unidade['distancia']:.2f} km</li>
            </ul>
        </div>
        """

        # Definir a cor: amarelo para os 5 mais próximos, vermelho para o restante
        cor = "orange" if i < 5 else "red"

        adicionar_ponto_unidade(mapa, unidade["latitude"], unidade["longitude"], descricao_completa, cor)

    # Renderizar o mapa como HTML
    mapa_html = mapa._repr_html_()

    # Passar o mapa e os hospitais mais próximos para o template
    return render(request, "map/mapa.html", {"mapa_html": mapa_html, "hospitais_proximos": unidades_mais_proximas})
