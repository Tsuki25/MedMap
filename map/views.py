from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.shortcuts import render
from geopy.distance import geodesic
import folium
from folium.plugins import LocateControl

from .forms import LoginForm
from .models import UnidadeAtendimento, Triagem, Sintoma, Usuario


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("map:mapa")  # Redireciona após login bem-sucedido

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        senha = form.cleaned_data["senha"]

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                self.request.session["usuario_id"] = usuario.id  # Simulando login
                messages.success(self.request, "Login realizado com sucesso!")
                return super().form_valid(form)
            else:
                messages.error(self.request, "Senha incorreta!")
                return self.form_invalid(form)
        except Usuario.DoesNotExist:
            messages.error(self.request, "Usuário não encontrado!")
            return self.form_invalid(form)

class MapaUnidadesView(TemplateView):
    template_name = "map/mapa.html"

    def get_user_coordinates(self):
        # Obtém as coordenadas do usuário a partir da requisição ou define valores padrão.
        lat_user = self.request.GET.get("lat_user")
        lon_user = self.request.GET.get("lon_user")

        if not lat_user or not lon_user:
            return -23.55, -46.63  # São Paulo como padrão

        return float(lat_user), float(lon_user)

    def adicionar_ponto_unidade(self, mapa, unidade, cor_marcador):
        # Adiciona um marcador de unidade de atendimento ao mapa.
        descricao_completa = f"""
        <div style='width: 200px;'>
            <h4 style='margin-bottom: 10px;'>{unidade['nome']}</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li><strong>Endereço:</strong> {unidade['endereco']}</li>
                <li><strong>Planos de Saúde:</strong> {unidade['planos_saude']}</li>
                <li><strong>Horário:</strong> {unidade['horario_atendimento']}</li>
                <li><strong>Fila:</strong> {unidade['fila']}</li>
                <li><strong>Especialidade:</strong> {unidade['especialidade']}</li>
                <li><strong>Distância:</strong> {unidade['distancia']:.2f} km</li>
            </ul>
        </div>
        """

        folium.Marker(
            location=[unidade["latitude"], unidade["longitude"]],
            popup=folium.Popup(descricao_completa, max_width=300),
            icon=folium.Icon(color=cor_marcador, icon='fa-hospital', prefix='fa')
        ).add_to(mapa)

    def get_unidades_ordenadas(self, coordenadas_usuario):
        # Busca as unidades de atendimento e as ordena pela distância do usuário.
        unidades = UnidadeAtendimento.objects.all()
        unidades_distancia = []

        for unidade in unidades:
            coordenadas_unidade = (unidade.endereco.latitude, unidade.endereco.longitude)
            distancia = geodesic(coordenadas_usuario, coordenadas_unidade).km

            unidades_distancia.append({
                "nome": unidade.nome,
                "latitude": unidade.endereco.latitude,
                "longitude": unidade.endereco.longitude,
                "endereco": unidade.endereco.__str__(),
                "planos_saude": ", ".join([convenio.nome_convenio for convenio in unidade.convenios.all()]),
                "horario_atendimento": unidade.horario_atendimento,
                "fila": unidade.lotacao_atual,
                "especialidade": unidade.especialidade,
                "distancia": distancia
            })

        return sorted(unidades_distancia, key=lambda x: x["distancia"])

    def get_context_data(self, **kwargs):
        # Monta o contexto do template, incluindo o mapa renderizado.
        context = super().get_context_data(**kwargs)
        coordenadas_usuario = self.get_user_coordinates()

        mapa = folium.Map(location=coordenadas_usuario, zoom_start=13)
        LocateControl(auto_start=True, keepCurrentZoomLevel=True, drawMarker=True, icon="fa-user", prefix="fa",
                      strings={"title": "Sua localização"}).add_to(mapa)

        unidades_ordenadas = self.get_unidades_ordenadas(coordenadas_usuario)
        unidades_mais_proximas = unidades_ordenadas[:5]
        unidades_carregadas = unidades_ordenadas[:100]

        for i, unidade in enumerate(unidades_carregadas):
            cor = "orange" if i < 5 else "red"
            self.adicionar_ponto_unidade(mapa, unidade, cor)

        context["mapa_html"] = mapa._repr_html_()
        context["hospitais_proximos"] = unidades_mais_proximas

        return context


class TriagemCreateView(CreateView):
    template_name = "triagem/triagem_geral.html"
    model = Triagem
    fields = ['peso', 'temperatura', 'pressao_sistolica', 'pressao_diastolica']

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO
        context = super().get_context_data(**kwargs)
        context['sintomas_gerais'] = Sintoma.objects.filter(parte_corpo="Geral")
        return context

    def form_valid(self, form):
        triagem = form.save(commit=False)  # Não salva ainda no banco de dados
        triagem.usuario = Usuario.objects.get(id=5)
        triagem.save()

        # Pega os sintomas gerais selecionados
        sintomas_gerais = self.request.POST.getlist('sintomas_gerais')

        # Associa os sintomas selecionados à triagem
        for sintoma in sintomas_gerais:
            sintoma_obj = Sintoma.objects.get(id=sintoma)
            triagem.sintomas.add(sintoma_obj)

        # Redireciona para a próxima página com o ID da triagem
        return super().form_valid(form)

    def get_success_url(self):
        # Depois que a triagem for salva, redireciona para a view de sintomas específicos
        return reverse_lazy('map:triagem_update', kwargs={'pk': self.object.pk})

class TriagemUpdateView(UpdateView):
    model = Triagem
    template_name = 'triagem/triagem_sintomas.html'
    fields = []  # Nenhum campo do modelo será diretamente editado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        triagem = self.object
        context['triagem'] = triagem
        context['sintomas_por_parte'] = {
            'cabeca': Sintoma.objects.filter(parte_corpo="Cabeça"),
            'tronco': Sintoma.objects.filter(parte_corpo="Tronco"),
            'braco': Sintoma.objects.filter(parte_corpo="Braços"),
            'perna': Sintoma.objects.filter(parte_corpo="Pernas"),
        }
        return context

    def form_valid(self, form):
        # Aqui você pode lidar com os sintomas específicos, que foram selecionados no segundo formulário
        triagem = form.save()

        # Pega os sintomas específicos do corpo selecionados
        sintomas_especificos = self.request.POST.getlist('sintomas_partes')

        # Associa os sintomas à triagem
        for sintoma in sintomas_especificos:
            sintoma_obj = Sintoma.objects.get(id=sintoma)
            triagem.sintomas.add(sintoma_obj)

        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona para uma página de confirmação ou outra view
        return reverse_lazy('map:mapa')