from django.contrib import admin

from map.models import Endereco, Convenio, UnidadeAtendimento

admin.site.register(Endereco)
admin.site.register(Convenio)
admin.site.register(UnidadeAtendimento)
