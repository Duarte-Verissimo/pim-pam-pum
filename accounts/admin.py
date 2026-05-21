from django import forms
from django.contrib import admin

from .models import EmailSettings, MagicLoginToken


@admin.register(MagicLoginToken)
class MagicLoginTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'used')
    list_filter = ('used', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('token', 'created_at')


class EmailSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = '__all__'
        widgets = {
            'host_password': forms.PasswordInput(render_value=True),
        }


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    form = EmailSettingsAdminForm
    list_display = (
        'host',
        'port',
        'use_tls',
        'host_user',
        'default_from_email',
        'is_active',
        'updated_at',
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        return not EmailSettings.objects.exists()

# No admin do Django, criar o grupo "gestor-portfolio" e atribuir permissoes
# add, view, change e delete para os modelos CRUD do portfolio: Projeto,
# Tecnologia, Competencia, Formacao e quaisquer outros modelos CRUD que venham
# a ser geridos por este grupo.
#
# Depois, criar/editar o utilizador gestor, associar ao grupo "gestor-portfolio"
# e marcar is_staff=True se esse utilizador tambem precisar de aceder ao admin.
