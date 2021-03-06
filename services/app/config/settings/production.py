from .base import *  # noqa: F401, F403


DEBUG = False
ALLOWED_HOSTS = ["pawnguild.xyz", "www.pawnguild.xyz"]
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True


EMAIL_USE_TLS = True
# EMAIL_PAGE_DOMAIN = ALLOWED_HOSTS[0] + "/"
EMAIL_PAGE_DOMAIN = "pawnguild.xyz" + "/"
