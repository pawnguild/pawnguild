from settings.base import *

ALLOWED_HOSTS = ["pawnhall.pythonanywhere.com"]
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "pawnhall7@gmail.com"
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_PASSWORD")
EMAIL_USE_TLS = True