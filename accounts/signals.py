from allauth.account.signals import user_logged_in, user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver

from artigos.utils import get_bloggers_group


GOOGLE_PROVIDER = 'google'


def _add_to_bloggers(user):
    if user and user.pk:
        user.groups.add(get_bloggers_group())


def _user_has_google_account(user):
    return (
        user
        and user.pk
        and user.socialaccount_set.filter(provider=GOOGLE_PROVIDER).exists()
    )


@receiver(user_signed_up)
def add_signed_up_user_to_bloggers(sender, request, user, **kwargs):
    _add_to_bloggers(user)


@receiver(user_logged_in)
def add_google_user_to_bloggers_on_login(sender, request, user, **kwargs):
    if _user_has_google_account(user):
        _add_to_bloggers(user)


@receiver(social_account_added)
@receiver(social_account_updated)
def add_google_social_user_to_bloggers(sender, request, sociallogin, **kwargs):
    if sociallogin.account.provider == GOOGLE_PROVIDER:
        _add_to_bloggers(sociallogin.user)
