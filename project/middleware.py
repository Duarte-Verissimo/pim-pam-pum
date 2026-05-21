from urllib.parse import urlsplit

from django.conf import settings


class PublicSiteUrlMiddleware:
    """Use SITE_URL when a production proxy forwards requests as localhost."""

    localhost_names = {"localhost", "127.0.0.1", "::1"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._apply_public_host(request)
        return self.get_response(request)

    def _apply_public_host(self, request):
        if not settings.SITE_URL:
            return

        public_url = urlsplit(settings.SITE_URL)
        if not public_url.scheme or not public_url.netloc:
            return

        raw_host = request.META.get("HTTP_HOST", "")
        if self._hostname(raw_host) not in self.localhost_names:
            return

        request.META["HTTP_HOST"] = public_url.netloc
        request.META["SERVER_NAME"] = public_url.hostname or public_url.netloc
        request.META["SERVER_PORT"] = str(
            public_url.port or (443 if public_url.scheme == "https" else 80)
        )
        request.META["wsgi.url_scheme"] = public_url.scheme
        request.META["HTTP_X_FORWARDED_PROTO"] = public_url.scheme

    def _hostname(self, raw_host):
        host = raw_host.split(",", 1)[0].strip().lower()
        if host.startswith("["):
            return host[1:].split("]", 1)[0]
        return host.split(":", 1)[0]
