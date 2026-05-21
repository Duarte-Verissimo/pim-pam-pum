from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from artigos.utils import BLOGGERS_GROUP_NAME

from .models import MagicLoginToken


@override_settings(
    STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
)
class MagicLoginTests(TestCase):
    def test_magic_login_uses_model_backend_and_consumes_token(self):
        user = User.objects.create_user(
            username='duarte',
            email='duarte@example.com',
            password='password123',
        )
        token = MagicLoginToken.objects.create(user=user, token='valid-token')

        response = self.client.get(reverse('magic_login_verify', args=[token.token]))

        self.assertRedirects(response, reverse('portfolio_home'))
        token.refresh_from_db()
        self.assertTrue(token.used)
        self.assertEqual(get_user(self.client), user)

    def test_used_magic_login_token_is_invalid(self):
        user = User.objects.create_user(
            username='duarte',
            email='duarte@example.com',
            password='password123',
        )
        token = MagicLoginToken.objects.create(
            user=user,
            token='used-token',
            used=True,
        )

        response = self.client.get(reverse('magic_login_verify', args=[token.token]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/magic_login_invalid.html')


@override_settings(
    STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
)
class BloggerGroupTests(TestCase):
    def test_registered_user_is_added_to_bloggers_group(self):
        response = self.client.post(
            reverse('registo'),
            {
                'username': 'ana',
                'email': 'ana@example.com',
                'first_name': 'Ana',
                'last_name': 'Silva',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
        )

        self.assertRedirects(
            response,
            reverse('login'),
            fetch_redirect_response=False,
        )
        user = User.objects.get(username='ana')
        self.assertTrue(user.groups.filter(name=BLOGGERS_GROUP_NAME).exists())

    def test_google_user_is_added_to_bloggers_group_on_allauth_login(self):
        user = User.objects.create_user(
            username='google-user',
            email='google@example.com',
        )
        SocialAccount.objects.create(
            user=user,
            provider='google',
            uid='google-uid',
        )

        user_logged_in.send(sender=self.__class__, request=None, user=user)

        self.assertTrue(user.groups.filter(name=BLOGGERS_GROUP_NAME).exists())
