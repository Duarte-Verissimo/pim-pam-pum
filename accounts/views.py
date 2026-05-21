import logging
import secrets

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.db import DatabaseError
from django.shortcuts import redirect, render
from django.urls import reverse

from artigos.utils import get_bloggers_group

from .forms import MagicLoginForm, RegistoForm
from .models import EmailSettings, MagicLoginToken


logger = logging.getLogger(__name__)


def login_view(request):
    erro = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('portfolio_home')

        erro = 'Credenciais inválidas'

    return render(request, 'accounts/login.html', {'erro': erro})


def logout_view(request):
    logout(request)
    return redirect('portfolio_home')


def registo_view(request):
    form = RegistoForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        user.groups.add(get_bloggers_group())
        return redirect('login')

    return render(request, 'accounts/registo.html', {'form': form})


def _gerar_token_unico():
    token = secrets.token_urlsafe(32)
    while MagicLoginToken.objects.filter(token=token).exists():
        token = secrets.token_urlsafe(32)
    return token


def _magic_login_email_options():
    try:
        email_settings = EmailSettings.objects.filter(pk=1, is_active=True).first()
    except DatabaseError:
        logger.exception("Could not load email settings from database")
        return {}

    if not email_settings or not email_settings.has_credentials:
        return {}

    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=email_settings.host,
        port=email_settings.port,
        username=email_settings.host_user,
        password=email_settings.host_password,
        use_tls=email_settings.use_tls,
        timeout=settings.EMAIL_TIMEOUT,
    )

    return {
        'connection': connection,
        'from_email': email_settings.default_from_email or email_settings.host_user,
    }


def magic_login_request(request):
    form = MagicLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user is not None:
            token = _gerar_token_unico()
            MagicLoginToken.objects.create(user=user, token=token)
            path = reverse('magic_login_verify', args=[token])
            link = f"{settings.SITE_URL}{path}" if settings.SITE_URL else request.build_absolute_uri(path)
            email_options = _magic_login_email_options()
            try:
                send_mail(
                    'Link de acesso ao portfolio',
                    f'Usa este link para entrar no portfolio: {link}\n\n'
                    'Este link expira em 15 minutos e so pode ser usado uma vez.',
                    email_options.get('from_email'),
                    [user.email],
                    fail_silently=False,
                    connection=email_options.get('connection'),
                )
            except Exception:
                logger.exception(
                    "Failed to send magic login email for user id %s",
                    user.pk,
                )

        messages.success(
            request,
            'Se existir uma conta associada a esse email, enviamos um link de acesso.',
        )
        return redirect('magic_login')

    return render(request, 'accounts/magic_login.html', {'form': form})


def magic_login_verify(request, token):
    token_obj = (
        MagicLoginToken.objects.select_related('user')
        .filter(token=token)
        .first()
    )

    if token_obj is None or not token_obj.is_valid():
        return render(request, 'accounts/magic_login_invalid.html')

    user = token_obj.user
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    token_obj.used = True
    token_obj.save(update_fields=['used'])
    return redirect('portfolio_home')
