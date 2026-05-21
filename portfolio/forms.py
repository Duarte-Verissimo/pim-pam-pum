from django import forms

from .models import Competencia, Formacao, Projeto, Tecnologia


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = "__all__"


class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = "__all__"


class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = "__all__"


class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = "__all__"
