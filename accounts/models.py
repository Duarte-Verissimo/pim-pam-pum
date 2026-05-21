from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class MagicLoginToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='magic_login_tokens',
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=15)
        return not self.used and timezone.now() <= expiration_time

    def __str__(self):
        return f"Magic token for {self.user.username}"


class EmailSettings(models.Model):
    host = models.CharField(max_length=255, default='smtp.gmail.com')
    port = models.PositiveIntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    host_user = models.EmailField(blank=True)
    host_password = models.CharField(max_length=255, blank=True)
    default_from_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'configuracao de email'
        verbose_name_plural = 'configuracoes de email'

    @property
    def has_credentials(self):
        return bool(self.is_active and self.host_user and self.host_password)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Configuracao de email'
