from django.shortcuts import render

import folium
from django.shortcuts import render
from .models import UnidadeAtendimento, Convenio

# Coordenadas do Usuário
coordenadas_usuario = [-23.1171, -46.5563]  # Pega as coordenadas do celular ou computador


def criar_mapa(request):
    # Criação do mapa centrado no Usuário
    mapa = folium.Map(location=coordenadas_usuario, zoom_start=13)

    # Função para adicionar um ponto no mapa
    def adicionar_ponto(mapa, latitude, longitude, nome, endereco, planos_saude, horario_atendimento, tempo_medio, fila,
                        especialidade):
        # Criação da descrição completa com formatação HTML
        descricao_completa = f"""
        <div style='width: 200px;'>
            <h4 style='margin-bottom: 10px;'>{nome}</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li><strong>Endereço:</strong> {endereco}</li>
                <li><strong>Planos de Saúde Aceitos:</strong> {planos_saude}</li>
                <li><strong>Horário de Atendimento:</strong> {horario_atendimento}</li>
                <li><strong>Tempo médio para Atendimento:</strong> {tempo_medio}</li>
                <li><strong>Pessoas aguardando:</strong> {fila}</li>
                <li><strong>Especialidade:</strong> {especialidade}</li>
            </ul>
        </div>
        """

        folium.Marker(  # Cria o ponto no mapa, pode ser formatado conforme desejado
            location=[latitude, longitude],
            popup=folium.Popup(descricao_completa, max_width=300),
            icon=folium.Icon(color='red', icon='fa-hospital', prefix='fa')
        ).add_to(mapa)

    # Buscar as unidades de atendimento no banco de dados
    unidades = UnidadeAtendimento.objects.all()

    # Adicionar os pontos no mapa
    for unidade in unidades:
        # Obter as convenções associadas à unidade
        convenios = unidade.convenio.all()
        planos_saude = ", ".join([convenio.nome_convenio for convenio in convenios])

        adicionar_ponto(
            mapa,
            unidade.endereco.latitude,  # latitude
            unidade.endereco.longitude,  # longitude
            unidade.nome,  # nome
            unidade.endereco.__str__(),  # endereço
            planos_saude,  # planos de saúde
            unidade.horario_atendimento,  # horário de atendimento
            unidade.tempo_medio_espera,  # tempo médio
            unidade.lotacao_atual,  # fila
            unidade.especialidade  # especialidade
        )

    # Salvar o mapa gerado em um arquivo HTML
    mapa_path = "map/templates/map/mapa.html"
    mapa.save(mapa_path)

    # Renderizar o mapa na tela
    return render(request, "map/mapa.html", {"mapa_path": mapa_path})

