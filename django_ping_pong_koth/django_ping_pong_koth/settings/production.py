from .base import *  # noqa : F403

ALLOWED_HOSTS += ["wolgamonox.pythonanywhere.com"]  # noqa : F405

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
