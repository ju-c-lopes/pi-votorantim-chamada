from django.contrib import admin
from core.models import *

# Register your models here.

class ShowTurma(admin.ModelAdmin):
    list_display = ('id_turma', 't_turma')

class ShowDis(admin.ModelAdmin):
    list_display = ('id', 'd_nome')

class ShowAula(admin.ModelAdmin):
    list_display = ('id_aula',)

class ShowAluno(admin.ModelAdmin):
    list_display = ('id_aluno', 'al_nome')

class ShowPres(admin.ModelAdmin):
    list_display = ('id_aula', 'id_presenca', 'data_aula', 'qte_aulas')

class ShowEscola(admin.ModelAdmin):
    list_display = ('id_escola', 'nome')

admin.site.register(Aluno, ShowAluno)
admin.site.register(Professor)
admin.site.register(Turma, ShowTurma)
admin.site.register(Disciplina, ShowDis)
admin.site.register(Aula, ShowAula)
admin.site.register(Presenca, ShowPres)
admin.site.register(Escola, ShowEscola)