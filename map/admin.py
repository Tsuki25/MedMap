from django.contrib import admin

from map.models import Endereco, Convenio, UnidadeAtendimento, Usuario, Condicao, Sintoma, Triagem, Doenca

admin.site.register(Endereco)
admin.site.register(Convenio)
admin.site.register(UnidadeAtendimento)
admin.site.register(Usuario)
admin.site.register(Condicao)
admin.site.register(Sintoma)
admin.site.register(Triagem)
admin.site.register(Doenca)