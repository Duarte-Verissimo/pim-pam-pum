from django.contrib import admin

# Register your models here.
from .models import Licenciatura, Docente, UnidadeCurricular, TipoTecnologia, Tecnologia, Projeto, TFC, Competencia, ExperienciaProfissional, MakingOf, Formacao


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('nome', 'sigla')


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'ects')
    search_fields = ('nome', 'sigla')


@admin.register(TipoTecnologia)
class TipoTecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel_interesse', 'url_oficial')
    list_filter = ('tipo', 'nivel_interesse')
    search_fields = ('nome', 'descricao', 'tipo__nome')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano')
    search_fields = ('titulo', 'descricao')


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano', 'nivel_interesse', 'licenciatura', 'parceiro')
    list_filter = ('nivel_interesse', 'licenciatura')
    search_fields = ('titulo', 'resumo', 'areas', 'palavras_chave')


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'nivel')
    list_filter = ('categoria',)
    search_fields = ('nome',)


@admin.register(ExperienciaProfissional)
class ExperienciaProfissionalAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'tipo', 'data_inicio', 'data_fim')
    list_filter = ('tipo', 'empresa')
    search_fields = ('cargo', 'empresa')


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_registo', 'entidade_referida')
    list_filter = ('data_registo',)
    search_fields = ('titulo', 'descricao', 'entidade_referida')


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instituicao', 'tipo', 'data_inicio', 'data_fim')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'instituicao')
