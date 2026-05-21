from django.urls import path

from . import views


urlpatterns = [
    path("", views.portfolio_view, name="portfolio_home"),
    path("sobre/", views.sobre_aplicacao_view, name="portfolio_sobre"),
    path("licenciaturas/", views.licenciaturas_view, name="portfolio_licenciaturas"),
    path("docentes/", views.docentes_view, name="portfolio_docentes"),
    path("disciplinas/", views.disciplinas_view, name="portfolio_disciplinas"),
    path("tecnologias/", views.tecnologias_view, name="portfolio_tecnologias"),
    path("tecnologias/nova/", views.nova_tecnologia_view, name="nova_tecnologia"),
    path(
        "tecnologias/<int:tecnologia_id>/edita/",
        views.edita_tecnologia_view,
        name="edita_tecnologia",
    ),
    path(
        "tecnologias/<int:tecnologia_id>/apaga/",
        views.apaga_tecnologia_view,
        name="apaga_tecnologia",
    ),
    path("projetos/", views.projetos_view, name="portfolio_projetos"),
    path("projetos/novo/", views.novo_projeto_view, name="novo_projeto"),
    path(
        "projetos/<int:projeto_id>/edita/",
        views.edita_projeto_view,
        name="edita_projeto",
    ),
    path(
        "projetos/<int:projeto_id>/apaga/",
        views.apaga_projeto_view,
        name="apaga_projeto",
    ),
    path("tfcs/", views.tfcs_view, name="portfolio_tfcs"),
    path("competencias/", views.competencias_view, name="portfolio_competencias"),
    path("competencias/nova/", views.nova_competencia_view, name="nova_competencia"),
    path(
        "competencias/<int:competencia_id>/edita/",
        views.edita_competencia_view,
        name="edita_competencia",
    ),
    path(
        "competencias/<int:competencia_id>/apaga/",
        views.apaga_competencia_view,
        name="apaga_competencia",
    ),
    path("formacoes/", views.formacoes_view, name="portfolio_formacoes"),
    path("formacoes/nova/", views.nova_formacao_view, name="nova_formacao"),
    path(
        "formacoes/<int:formacao_id>/edita/",
        views.edita_formacao_view,
        name="edita_formacao",
    ),
    path(
        "formacoes/<int:formacao_id>/apaga/",
        views.apaga_formacao_view,
        name="apaga_formacao",
    ),
    path("experiencias/", views.experiencias_view, name="portfolio_experiencias"),
    path("making-of/", views.making_of_view, name="portfolio_making_of"),
]
