from django.db import models

class Endereco(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=200)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"


class Convenio(models.Model):
    nome_convenio = models.CharField(max_length=75)

    def __str__(self):
        return self.nome_convenio


class UnidadeAtendimento(models.Model):
    nome = models.CharField(max_length=200)
    horario_atendimento = models.CharField(max_length=13)
    especialidade = models.CharField(max_length=75)
    lotacao_atual = models.IntegerField()
    tempo_medio_espera = models.DurationField()
    endereco = models.OneToOneField(
        Endereco, on_delete=models.CASCADE, related_name="unidade_atendimento"
    )
    convenio = models.ManyToManyField(Convenio)

    def __str__(self):
        return self.nome
