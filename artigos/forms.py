from django import forms

from .models import Artigo, Comentario, Rating


class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome_visitante', 'texto']
        labels = {
            'nome_visitante': 'Nome',
            'texto': 'Comentario',
        }

    def __init__(self, *args, mostrar_nome_visitante=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not mostrar_nome_visitante:
            self.fields.pop('nome_visitante')
        else:
            self.fields['nome_visitante'].required = False
            self.fields['nome_visitante'].help_text = 'Opcional.'

    def clean_nome_visitante(self):
        return self.cleaned_data.get('nome_visitante', '').strip()


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['pontuacao']
        labels = {
            'pontuacao': 'Pontuacao',
        }
        widgets = {
            'pontuacao': forms.Select(),
        }
