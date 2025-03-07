from django.db import models

class Convenio(models.Model):
    nome_convenio = models.CharField(max_length=45)
    def __str__(self):
        return self.nome_convenio

class Endereco(models.Model):
    latitude = models.DecimalField(max_digits=7, decimal_places=5)
    longitude = models.DecimalField(max_digits=7, decimal_places=5)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=75)
    numero = models.CharField(max_length=15)
    bairro = models.CharField(max_length=45)
    cidade = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    pais = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"

class UnidadeAtendimento(models.Model):
    nome = models.CharField(max_length=75)
    horario_atendimento = models.CharField(max_length=75)
    especialidade = models.CharField(max_length=120)
    lotacao_atual = models.IntegerField()
    tempo_medio_espera = models.TimeField()
    convenios = models.ManyToManyField(Convenio)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, related_name="unidade_atendimento")

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome_usuario = models.CharField(max_length=45)
    sobrenome_usuario = models.CharField(max_length=100)
    dt_nasc = models.DateField()
    altura = models.DecimalField(max_digits=3, decimal_places=2)
    dt_cadastro = models.DateField()
    convenio = models.ForeignKey(Convenio, on_delete=models.SET_NULL, null=True, blank=True)
    condicoes = models.ManyToManyField('Condicao')

    def __str__(self):
        return self.nome_usuario

class Condicao(models.Model):
    nome_condicao = models.CharField(max_length=45)
    gravidade = models.IntegerField()
    def __str__(self):
        return self.nome_condicao

class Sintoma(models.Model):
    nome_sintoma = models.CharField(max_length=45)

    def __str__(self):
        return self.nome_sintoma

class Triagem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura = models.DecimalField(max_digits=3, decimal_places=1)
    pressao_sistolica = models.IntegerField()
    pressao_diastolica = models.IntegerField()
    gravidez = models.IntegerField()
    horario_realizacao = models.TimeField()
    data_realizacao = models.DateField()
    sintomas = models.ManyToManyField(Sintoma)

    def __str__(self):
        return f"{self.usuario.nome_usuario} - {self.data_realizacao} - {self.horario_realizacao} "